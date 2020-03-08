import requests
import datetime
from random import randint
import json
from functools import reduce


def telegram_bot_sendAvviso(bot_chatID,bot_message):
    bot_token = '1089624955:AAFOClqR9FeHz-2mQBWBf0XqMfjbpnj8VK4'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    #return response.json()


#telegram_bot_sendAvviso('289128883',"Ciao!")
#print(test)


def mensa_pasti(mensa_target="apollonia"):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'}
    url = "https://www.dsu.toscana.it/servizi/ristorazione/dove-e-cosa-mangiare/i-menu/"

    source_page = requests.get(url, headers=headers).text
    source_page = source_page.split('<div id="dslc-theme-content-inner">')[1]
    source_page = source_page.split('<strong>FIRENZE<br />\nMensa Caponnetto e Calamandrei<br />\n</strong>')[1]
    source_page = source_page.split('<a href="')

    link_mense = ""
    url_used = []
    for i in range(1,15):
        mensa = source_page[i].split('"')[0]
        if mensa_target in mensa:
            giorno = int(mensa.split("dal-")[1].split("-al")[0].split(".")[0])
            mese = int(mensa.split("dal-")[1].split("-al")[0].split(".")[1])
            anno = int(mensa.split("dal-")[1].split("-al")[0].split(".")[2]) + 2000
            data_inizio = (anno, mese, giorno)
            giorno = int(mensa.split("al-")[2].split("-")[0].split(".")[0])
            mese = int(mensa.split("al-")[2].split("-")[0].split(".")[1])
            anno = int(mensa.split("al-")[2].split("-")[0].split(".")[2]) + 2000
            data_fine = (anno, mese, giorno)
            today = (datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
            if data_inizio <= today <= data_fine and mensa not in url_used:
                link_mense += mensa + "\n"
                url_used.append(mensa)

    return link_mense




