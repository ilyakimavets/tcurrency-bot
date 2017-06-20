import os
import datetime

default = 'RUB'

min_amount = 0.01

convert_api_url = 'http://free.currencyconverterapi.com/api/v3/convert?q={currency_from}_{currency_to}&compact=ultra'

list_url = 'http://free.currencyconverterapi.com/api/v3/currencies'
list_cache = 'supported_currencies.json'
list_cache_update_delta = datetime.timedelta(days=7)