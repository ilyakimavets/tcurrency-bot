import supycache
import requests

from settings import CONVERT_API_URL, LIST_API_URL


@supycache.supycache(cache_key='all_currencies', max_age=60 * 60 * 3)  # Cache for 3 hours
def get_all():
    r = requests.get(LIST_API_URL)
    j = r.json().get('results')
    if j:
        return j
    else:
        raise ValueError('List of all currencies API response has no expected data')


@supycache.supycache(cache_key='{0}_support', max_age=60 * 60 * 1)  # Cache for 1 hour
def is_supported(currency):
    return currency in get_all()


@supycache.supycache(cache_key='{0}_{1}_ratio', max_age=60 * 10)  # Cache for 10 minutes
def get_ratio(currency_from, currency_to):
    params = {'q': f'{currency_from}_{currency_to}', 'compact': 'ultra'}
    r = requests.get(CONVERT_API_URL, params=params)
    j = r.json()
    ratio = list(j.values())[0]
    return ratio


def convert(currency_from, currency_to, amount):
    supported = all([is_supported(currency_from), is_supported(currency_to)])
    if supported:
        ratio = get_ratio(currency_from, currency_to)
        result = ratio * amount
        return result
