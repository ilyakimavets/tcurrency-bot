import logging
import re
from uuid import uuid4

from telegram import ParseMode, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, InlineQueryHandler

from currency import convert, is_supported

import strings
import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# helpers
def _build_rates_list(rates):
    response = [f'{cur} = {rates[cur]:.4f} ' if rates[cur] else f'{cur} - not supported' for cur in rates]
    return response


def _build_full_response(data):
    heading = '{amount} {from_currency}:'.format(amount=data['amount'], from_currency=data['from_currency'])
    body = '\n'.join(f'• {item}' for item in _build_rates_list(data['to_currencies']))
    response = '\n'.join([heading, body])
    return response


def _currency_handler(args):
    if len(args) < 1:
        return strings.BAD_FORMAT

    from_match = re.match(r'^(?P<amount>\d+(?:(?:[.,])\d+)?)?(?P<currency>\w{3})$', args[0])
    if not from_match:
        return strings.BAD_FORMAT

    from_dict = from_match.groupdict()
    from_currency = from_dict.get('currency')

    if not is_supported(from_currency):
        return strings.BAD_CURRENCY_MESSAGE.format(currency=from_currency, api_provider_url=settings.API_PROVIDER_URL)

    match_amount = from_dict.get('amount')
    if not match_amount:
        amount = 1.0
    else:
        match_amount = float(match_amount.replace(',', '.'))
        if match_amount > settings.MINIMAL_AMOUNT:
            amount = match_amount
        else:
            return strings.BAD_AMOUNT_MESSAGE

    to_currencies = {}

    if len(args) == 1:
        if from_currency == settings.DEFAULT_CURRENCY:
            return strings.DEFAULT_CURRENCY_MESSAGE.format(default_currency=settings.DEFAULT_CURRENCY)
        to_currencies[settings.DEFAULT_CURRENCY] = convert(from_currency, settings.DEFAULT_CURRENCY, amount)
    else:
        for to_arg in args[1:]:
            to_match = re.match(r'^(?P<currency>\w{3})$', to_arg)
            if not to_match:
                continue
            to_currency = to_match.groupdict().get('currency')
            if not is_supported(to_currency):
                return strings.BAD_CURRENCY_MESSAGE.format(currency=to_currency,
                                                           api_provider_url=settings.API_PROVIDER_URL)
            to_currencies[to_currency] = convert(from_currency, to_currency, amount)
        if not to_currencies:
            return strings.BAD_FORMAT

    return {'from_currency': from_currency, 'to_currencies': to_currencies, 'amount': amount}


def start(bot, update):
    update.message.reply_text(strings.HELP_MESSAGE, parse_mode=ParseMode.MARKDOWN)


def inline(bot, update):
    query = update.inline_query.query
    if not query:
        return

    args = []
    for arg in query.upper().split():
        if arg not in args:
            args.append(arg)

    data = _currency_handler(args)
    if isinstance(data, str):
        title = 'Error'
        description = data
        response = data
    else:
        title = '{amount} {currency}'.format(amount=data['amount'], currency=data['from_currency'])
        description = ', '.join(_build_rates_list(data['to_currencies']))
        response = _build_full_response(data)

    results = [InlineQueryResultArticle(id=uuid4(), title=title, description=description,
                                        input_message_content=InputTextMessageContent(response,
                                                                                      disable_web_page_preview=True))]
    update.inline_query.answer(results)


def log_error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def show_messages(bot, update):
    print(f'{update.message.from_user.username}: {update.message.text}')


def main():
    updater = Updater(settings.TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(InlineQueryHandler(inline))

    dp.add_error_handler(log_error)

    if settings.ENV == 'prod':
        updater.start_webhook(listen='0.0.0.0', port=settings.PORT, url_path=settings.TOKEN)
        updater.bot.set_webhook(settings.URL + settings.TOKEN)
    else:
        updater.start_polling(poll_interval=1)

    updater.idle()


if __name__ == '__main__':
    main()
