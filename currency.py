import json
import os
from datetime import datetime

import requests

from settings.currency import (convert_api_url, list_url, list_cache,
                               list_cache_update_delta)


def get_supported_list():
    r_json = requests.get(list_url).json()
    return r_json


def get_list_cache():
    try:
        time_since_modified = datetime.fromtimestamp(os.path.getmtime(list_cache))
    except FileNotFoundError:
        supported_list = update_list_cache()
    else:
        if (datetime.now() - time_since_modified) >= list_cache_update_delta:
            supported_list = update_list_cache()
        else:
            with open(list_cache) as f:
                supported_list = json.load(f)
    return supported_list


def update_list_cache():
    supported_list = get_supported_list()
    with open(list_cache, 'w+') as f:
        json.dump(supported_list, f)
    return supported_list


def is_supported(*currencies):
    supported_list = get_list_cache()
    if all(curr in supported_list['results'] for curr in currencies):
        return True
    return False


def get_currency(currency_from, currency_to):
    r_json = requests.get(convert_api_url.format(currency_from=currency_from, currency_to=currency_to)).json()
    currency = list(r_json.values())[0]
    return currency


def convert(currency_from, currency_to, amount):
    if is_supported(currency_from, currency_to):
        currency = get_currency(currency_from, currency_to)
        result = currency * amount
        return result
