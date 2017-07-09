import supycache
import requests

from settings import CONVERT_API_URL, LIST_API_URL


@supycache.supycache(cache_key='all_currencies', max_age=60 * 60 * 4)  # Cache for 4 hours
def get_all():
    r = requests.get(LIST_API_URL)
    j = r.json().get('results')
    if j:
        return j
    else:
        raise ValueError('List of all currencies API response has no expected data')


@supycache.supycache(cache_key='{0}_support', max_age=60 * 60 * 2)  # Cache for 2 hours
def is_supported(currency):
    return currency in get_all()


@supycache.supycache(cache_key='{0}_{1}_ratio', max_age=60 * 30)  # Cache for 30 minutes
def get_ratio(currency_from, currency_to):
    params = {'q': f'{currency_from}_{currency_to}', 'compact': 'ultra'}
    r = requests.get(CONVERT_API_URL, params=params)
    j = r.json()
    ratio = list(j.values())[0]
    return ratio


def convert(currency_from, currency_to, amount):
    ratio = get_ratio(currency_from, currency_to)
    result = ratio * amount
    return result
