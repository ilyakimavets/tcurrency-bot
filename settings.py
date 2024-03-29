import os

CONVERT_API_URL = 'http://free.currencyconverterapi.com/api/v3/convert'
LIST_API_URL = 'http://free.currencyconverterapi.com/api/v3/currencies'
API_PROVIDER_URL = 'http://free.currencyconverterapi.com/'

DEFAULT_CURRENCY = 'RUB'
MINIMAL_AMOUNT = 0.1

TOKEN = os.environ.get('TELEGRAM_TOKEN')
ENV = os.environ.get('ENV')
URL = os.environ.get('URL')
PORT = int(os.environ.get('PORT', '5000'))