START_MESSAGE = '''
*Hello!*

This bot will help you to *convert currencies* via Telegram.

/help — *bot usage*
/example — *bot usage example*
/list — *list of supported currencies*
'''
RESULT_MESSAGE = '{amount} {cur1} = {result} {cur2}'
USAGE_MESSAGE = 'Usage: `/c arg1 [arg2]`'
LIST_MESSAGE = '{currency} - {currency_name} ({currency_symbol})'
EXAMPLE_MESSAGE = 'Example: `/c 15USD EUR` or `/c 25EUR` or `/c UAH`'
BAD_FORMAT = 'Incorrect format. See /help and /example and try again.'
BAD_CURRENCY_MESSAGE = 'Incorrect currency. See /support for the list of supported currencies.'
BAD_AMOUNT_MESSAGE = 'Incorrect amount of currency. It must be higher than 0.01 or empty (will be handled as 1).'
