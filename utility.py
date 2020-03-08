import requests
import datetime
from random import randint
import json


def telegram_bot_sendAvviso(bot_chatID,bot_message):
    bot_token = '1089624955:AAFOClqR9FeHz-2mQBWBf0XqMfjbpnj8VK4'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)


def getSchedules(ora_inizio):
    ora_inizio_dict = {8: 2, 8.5: 3, 14: 14}
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'}
    url = "https://siprad.unifi.it/index.php?plesso=14"

    source_page = requests.get(url, headers=headers).text
    piani = source_page.split('<div class="titolo_edificio" style="margin-top:20px">')
    piani.pop(0)
    piani.pop(-1)

    free_schedule = {}
    for piano in piani:
        nome_piano = piano.split(" -")[0]
        #print(nome_piano)
        piano = piano.split("<tr >")
        piano.pop(0)
        for aula in piano:
            col = aula.split("<td")
            nome_aula = col[1].split(">")[1].split("<")[0]
            free_schedule[nome_aula] = []
            ora = 7.5
            fascia_oraria_libera = ora_inizio
            #print(nome_aula)
            for i in range(2,len(col)):
                if col[i].startswith(" class='col_ora'"):
                    # occupata
                    occupazione_ore = int(col[i].split("colspan='")[1].split("'")[0])/2
                    #print("Occupata ", ora, "-", ora + occupazione_ore)
                    if fascia_oraria_libera != ora and ora > ora_inizio:
                        #print("Libera ",fascia_oraria_libera," - ", ora)
                        free_schedule[nome_aula].append([fascia_oraria_libera,ora])
                    ora += occupazione_ore
                    if ora > ora_inizio:
                        fascia_oraria_libera = ora
                else:
                    ora += 0.5
                if i == len(col) - 1:
                    if fascia_oraria_libera != ora:
                        #print("Libera ", fascia_oraria_libera, " - ", ora)
                        free_schedule[nome_aula].append([fascia_oraria_libera,ora])

    return free_schedule


def ranking_aule(top_n=30):
    aule_libere = getSchedules(ora_inizio=int(datetime.datetime.now().hour)+1)
    top_aule_libere = {}

    for i in range(top_n):
        max_intervallo_ore = 0
        for aula in aule_libere:
            #print(aula)
            if aula not in ["_x_ ", "Aula Informatica 109 ", "Aula Informatica 110 ", "Aula Informatica 111 ", "Aula Informatica 112 ", "Aula Informatica 113 ",
                            "Aula Informatica 115 ", "Aula Informatica 116 ", "Aula informatica 116 ", "Aula Disegno 107 ", "AUla 011 ", "Aula 214 ", "Aula 207 ", "Aula Disegno 108 ", "Aula Magna 327 ", "Anfiteatro "]:
                for intervallo in aule_libere[aula]:
                    #print(intervallo)
                    intervallo_libero_ore = intervallo[1] - intervallo[0]
                    if intervallo_libero_ore > max_intervallo_ore:
                        max_intervallo_ore = intervallo_libero_ore
                        max_intervallo = [intervallo[0], intervallo[1]]
                        max_aula = aula
        aule_libere[max_aula].remove(max_intervallo)
        if max_aula not in top_aule_libere:
            top_aule_libere[max_aula] = []
        top_aule_libere[max_aula].append(max_intervallo)
    display_top_aule_libere = ""
    for piano in range(0,4):
        display_top_aule_libere += "--------------------  Piano "+str(piano)+"  -------------------\n"
        for aula in top_aule_libere:
            if aula.startswith("Aula "+str(piano)) or aula.startswith("AUla "+str(piano)):
                display_top_aule_libere += aula + " - " + str(top_aule_libere[aula]) + "\n"
            elif piano == 0 and aula == "Auditorium A ":
                display_top_aule_libere += aula + " - " + str(top_aule_libere[aula]) + "\n"
            elif piano == 1 and aula == "Auditorium B ":
                display_top_aule_libere += aula + " - " + str(top_aule_libere[aula]) + "\n"
    return display_top_aule_libere


def mensa_pasti(mensa_target="calamandrei"):
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


def citazioniUrl():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'}
    url = "https://aforisticamente.com/elenco-autori-di-aforismi/frasi-citazioni-e-aforismi-temi-piu-popolari/"

    source_page = requests.get(url, headers=headers).text
    source_page = source_page.split('<div class="mkd-page-content-holder mkd-grid-col-8">')[1]
    source_page = source_page.split('<a href="https://aforisticamente.com/2')
    source_page.pop(0)

    urlsCitazioni = []
    for topic in source_page:
        topic = topic.split('"')[0]
        urlsCitazioni.append("https://aforisticamente.com/2"+topic)

    return urlsCitazioni


def citazioni():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'}
    url = citazioniUrl()
    url = url[randint(0, len(url) - 1)]

    source_page = requests.get(url, headers=headers).text
    source_page = source_page.split('<div class="mkd-post-text-main">')[1]
    source_page = source_page.split('<ins class="adsbygoogle" style="display:inline-block;width:336px;height:280px" data-ad-client="ca-pub-9436777233069869" data-ad-slot="5867361830"></ins>')[0]
    citazioni = source_page.split('<p>')
    for i in range(4):
        citazioni.pop(0)
    todayCitazioni = []

    for citazione in citazioni:
        citazione = citazione.split('</p>')[0]
        citazione = citazione.replace('<br />','\n')
        citazione = citazione.replace('&#8217;',"'")
        citazione = citazione.replace('&#8220;','"')
        citazione = citazione.replace('&#8221;','"')
        citazione = citazione.replace('&#8230;','...')
        citazione = citazione.replace('&amp;','&')
        citazione = citazione.replace('&#8211;','-')
        citazione = citazione.replace('<em>','')
        citazione = citazione.replace('</em>','')
        todayCitazioni.append(citazione)
    return todayCitazioni





def avvisiProf(listaProf):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'}
    url = "https://www.ingegneria.unifi.it/avvisi.html"

    source_page = requests.get(url, headers=headers).text
    source_page = source_page.split('<div id="mdbache-container">')[1]
    avvisi = source_page.split('<div class="mdbache-avviso" style="margin-bottom: 10px;">')
    avvisi.pop(0)

    avvisiJson = {"avvisi" : []}

    for avviso in avvisi:
        professore = avviso.split("\n</h2>")[0].split(">\n")[1]
        if professore in listaProf:
            titolo = avviso.split("\n</h2>")[1].split(">\n")[1].replace("&amp;","")
            messaggio = avviso.split('</div>')[0].split('<div class="mdbache-avvisocorpo">')[1].replace("&amp;", "")
            data = avviso.split('</div>')[1].split('>')[1]
            avvisiJson["avvisi"].append({"professore":professore,"titolo":titolo,"messaggio":messaggio,"data":data})
    return avvisiJson


def checkNewAvvisi(listaProf):
    with open("./avvisiProf.json", "r") as f:
        oldAvvisi = json.load(f)["avvisi"]
        webSiteAvvisi = avvisiProf(listaProf)["avvisi"]
        newAvvisi = [x for x in webSiteAvvisi if x not in oldAvvisi]
        avvisiJson = {"avvisi": webSiteAvvisi}
        with open ("./avvisiProf.json", "w") as f:
            json.dump(avvisiJson,f)
        for avviso in newAvvisi:
            professore = avviso["professore"]
            titolo = avviso["titolo"]
            messaggio = avviso["messaggio"]
            data = avviso["data"]
            notification = professore + "\n" + titolo + "\n" + messaggio + data
            telegram_bot_sendAvviso('289128883', notification)
            # -183782909 Telegram e' meglio
            # 289128883 Abdullah
            # -378839483 gruppo 'Uu'



def avvisi():
    listaProf = ["A.  Piva", "A.  Luchetta", "S.  Marinai", "P.  Pala", "S.  Berretti", "M.  Basso", "F.  Schoen",
                 "G.  Battistelli", "M.  Bertini", "M.  Serena", "P.  Bellini", "R.  Fantacci", "E.  Boni", "P.  Nesi",
                 "A.  Fantechi"]
    checkNewAvvisi(listaProf)