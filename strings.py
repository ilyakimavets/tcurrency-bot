START_MESSAGE = '''This bot can convert currencies.

*Commands:*
/help — get bot usage information
/example — get bot usage examples
/support — get a link where all supported currencies are avaliable'''
HELP_MESSAGE = '*Usage:* `/c arg1 [arg2]`'
SUPPORT_MESSAGE = 'List of supported currencies is avaliable at the ["Free Currency Converter API" website]({api_provider_url}).'
EXAMPLE_MESSAGE = '''*Examples:*
`/c 15USD EUR` — convert 15 USD to EUR
`/c 25EUR` — convert 25 EUR to default bot currency ({default_currency})
`/c UAH` — convert 1 UAH to default bot currency ({default_currency}); since amount is not specified, it will be handled as 1'''
RESULT_MESSAGE = '{amount} {cur1} = {result} {cur2}'
BAD_FORMAT = 'Incorrect format. See /help and /example, then try again.'
BAD_CURRENCY_MESSAGE = 'Incorrect currency. See /support for the list of supported currencies.'
BAD_AMOUNT_MESSAGE = 'Incorrect amount of currency. It must be higher than {minimal_amount} or empty (will be handled as 1).'
