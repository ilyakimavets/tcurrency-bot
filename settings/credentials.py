import os


def get_token():
    _token = os.environ.get('TELEGRAM_TOKEN')
    if _token is None:
        raise EnvironmentError('Token was not found in Environment Variables')
    return _token
TOKEN = get_token()