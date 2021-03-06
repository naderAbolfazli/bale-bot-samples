import logging

from telegram import Bot, LabeledPrice
from telegram.ext import Updater, CommandHandler, RegexHandler, ConversationHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

INVOICE = 0


def start(bot: Bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="what amount of money?")
    return INVOICE


def invoice(bot, update):
    bot.send_invoice(chat_id=update.message.chat_id, title="title", description="description", payload="payload",
                     provider_token="6037603760376037", start_parameter="", currency="IRR",
                     prices=[LabeledPrice('label1', int(update.message.text))])
    return ConversationHandler.END


updater = Updater(token='Token',
                  base_url="https://tapi.bale.ai/")

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={
        INVOICE: [RegexHandler(pattern='^\d+$', callback=invoice)],
    },

    fallbacks=[]
)

updater.dispatcher.add_handler(conversation_handler)

updater.bot.delete_webhook()
updater.start_polling(poll_interval=2)
# you can replace above line with commented below lines to use webhook instead of polling
# updater.start_webhook(listen=os.getenv('WEB_HOOK_IP', ""), port=int(os.getenv('WEB_HOOK_PORT', "")),
#                       url_path=os.getenv('WEB_HOOK_PATH', ""))
# updater.bot.set_webhook(url="{}{}".format(os.getenv('WEB_HOOK_DOMAIN', ""), os.getenv('WEB_HOOK_PATH', "")))
updater.idle()
