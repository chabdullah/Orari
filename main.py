from random import randint
import telegram
from telegram.ext import Updater, MessageHandler, Filters
import logging
from telegram.ext import CommandHandler
from utility import ranking_aule, mensa_pasti, citazioni, avvisi
import datetime


bot = telegram.Bot(token='1089624955:AAFOClqR9FeHz-2mQBWBf0XqMfjbpnj8VK4')
#print(bot.get_me())


updater = Updater(token='1089624955:AAFOClqR9FeHz-2mQBWBf0XqMfjbpnj8VK4', use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao!\n"
                                                                    "/orario per vedere le aule libere di oggi al Morgagni\n"
                                                                    "/mensacala per la mensa del Calamandrei\n"
                                                                    "/mensasesto per la mensa di Sesto\n"
                                                                    "/mensaapollonia per la mensa di Sant'Apollonia\n")


def info(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="/orario per vedere le aule libere di oggi al Morgagni\n"
                                                                    "/mensacala per la mensa del Calamandrei\n"
                                                                    "/mensasesto per la mensa di Sesto\n"
                                                                    "/mensaapollonia per la mensa di Sant'Apollonia\n")


def orario(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=ranking_aule())


def mensa_calamandrei(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensa_pasti("calamandrei"))


def mensa_sesto(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensa_pasti("sesto"))


def mensa_apollonia(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensa_pasti("apollonia"))


def echoMensa(update, context):
    if update.effective_chat.id not in [-183782909, 289128883]:
        bot.send_message(chat_id=289128883, text=str(update.effective_chat) + "\n" + str(update.message["text"]))
    response = ""
    orario = int(datetime.datetime.now().hour)+1
    if (11 <= orario <= 13) and any(substring in update.message.text.lower() for substring in ['mensa', "pranz", "mangia", "pappia", "pappa", "mensiamo", "cibo"]):
        response = citazioni()
        response = response[randint(0, len(response) - 1)]
    elif any(substring in update.message.text.lower() for substring in ["che fine ha fatto"]):
        response = ["Per me è morto...", "Per me è ancora in circolazione..."]
        response = response[randint(0, len(response) - 1)]
    try:
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    except:
        pass


def unknown(update, context):
    unknown_message = ["Mh?","Come?", "Eh?"]
    unknown_message = unknown_message[randint(0,len(unknown_message)-1)]
    context.bot.send_message(chat_id=update.effective_chat.id, text=unknown_message)


#Jobs
def avvisiJob(context: telegram.ext.CallbackContext):
    avvisi()


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

info_handler = CommandHandler('info', info)
dispatcher.add_handler(info_handler)

schedule_handler = CommandHandler('orario', orario)
dispatcher.add_handler(schedule_handler)

mensa_calamandrei_handler = CommandHandler('mensacala', mensa_calamandrei)
dispatcher.add_handler(mensa_calamandrei_handler)

mensa_sesto_handler = CommandHandler('mensasesto', mensa_sesto)
dispatcher.add_handler(mensa_sesto_handler)

mensa_apollonia_handler = CommandHandler('mensaapollonia', mensa_apollonia)
dispatcher.add_handler(mensa_apollonia_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

echoMensa_handler = MessageHandler(Filters.text, echoMensa)
dispatcher.add_handler(echoMensa_handler)

job_minute = j.run_repeating(avvisiJob, interval=14600, first=0)

updater.start_polling()
