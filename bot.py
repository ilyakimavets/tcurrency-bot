import logging
import re

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from currency import convert
from strings import USAGE_MESSAGE, EXAMPLE_MESSAGE, BAD_CURRENCY_MESSAGE, BAD_FORMAT, RESULT_MESSAGE, \
    BAD_AMOUNT_MESSAGE, LIST_MESSAGE, START_MESSAGE
from settings.credentials import TOKEN
from settings.currency import default as default_currency, min_amount, api_provider_url

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text(START_MESSAGE, parse_mode=ParseMode.MARKDOWN)


def help(bot, update):
    update.message.reply_text(USAGE_MESSAGE, parse_mode=ParseMode.MARKDOWN)


def example(bot, update):
    update.message.reply_text(EXAMPLE_MESSAGE, parse_mode=ParseMode.MARKDOWN)


def c_list(bot, update):
    result = 'List of supported currencies is avaliable at: ' + api_provider_url
    update.message.reply_text(result, disable_web_page_preview=True)


def currency(bot, update, args):
    if len(args) not in (1, 2):
        update.message.reply_text(BAD_FORMAT)
        return

    arg1_match = re.match(r'^(?P<amount>\d+(?:(?:[.,])\d+)?)?(?P<currency>\w{3})$', args[0].strip())
    if arg1_match:
        arg1 = arg1_match.groupdict()
    else:
        update.message.reply_text(BAD_FORMAT)
        return

    _amount = arg1.get('amount')
    # AMOUNT: if amount is in user input, check the minimum value and convert to float
    if _amount:
        _amount = float(_amount.replace(',', '.'))
        if _amount > min_amount:
            amount = _amount
        else:
            update.message.reply_text(BAD_AMOUNT_MESSAGE)
            return
    # AMOUNT: if not, then set it to 1
    else:
        amount = 1

    cur1 = arg1.get('currency').upper()
    cur2 = default_currency

    if len(args) == 2:
        arg2_match = re.match(r'^(?P<currency>\w{3})$', args[1].strip())
        if arg2_match:
            arg2 = arg2_match.groupdict()
        else:
            update.message.reply_text(BAD_FORMAT)
            return

        cur2 = arg2.get('currency').upper()

    result = convert(cur1, cur2, amount)
    if result is not None:
        update.message.reply_text(RESULT_MESSAGE.format(amount=amount, cur1=cur1, result=result, cur2=cur2))
    else:
        update.message.reply_text(BAD_CURRENCY_MESSAGE)


def log_error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def show_messages(bot, update):
    print(f'{update.message.from_user.username}: {update.message.text}')


def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("example", example))
    dp.add_handler(CommandHandler('list', c_list))
    dp.add_handler(CommandHandler('c', currency, pass_args=True))

    dp.add_handler(MessageHandler(Filters.text, show_messages))

    dp.add_error_handler(log_error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
