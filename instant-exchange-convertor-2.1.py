import re
from requests import get
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup

now = datetime.now()
time = datetime.strftime(now, "\n%d-%B-%Y\t%H:%M:%S:%f\n")

types = {
    "dollar": {
        "name": "DOLAR",
        "path": "/serbest-piyasa/amerikan-dolari",
        "tag": "div",
        "class": "market-data",
        "regex": "DOLAR(\S+)"
    },
    "pound": {
        "name": "STERLIN/POUND",
        "path": "/serbest-piyasa/amerikan-dolari",
        "tag": "div",
        "class": "market-data",
        "regex": "STERLİN(\S+)"
    },
    "gram_gold": {
        "name": "GRAM GOLD",
        "path": "/serbest-piyasa/amerikan-dolari",
        "tag": "div",
        "class": "market-data",
        "regex": "ALTIN(\S+)"
    },
    "euro": {
        "name": "EURO",
        "path": "/serbest-piyasa/amerikan-dolari",
        "tag": "div",
        "class": "market-data",
        "regex": "EURO(\S+)"
    }
}

types_2 = {
    "bitcoin": {
        "name": "BITCOIN",
        "path": "/kripto-paralar/bitcoin",
        "tag": "ul",
        "class": "piyasa-ozeti",
        "regex": "Bitcoin\s+%\s-?[\d,]+\s+\$?([\d\.,]+)"
    }
}


def exc_try():
    for typ in types:
        exchangeURL = "https://kur.doviz.com" + types[typ]["path"]
        r = get(exchangeURL)
        soup = BeautifulSoup(r.content, "html.parser")

        marketSumForex = soup.find_all("div", {"class": "market-data"})
        divs = soup.find_all(types[typ]["tag"], {types[typ]["class"]})
        all_texts = divs[-1].text
        raw_text = all_texts.replace("\n", "")
        value = re.findall(types[typ]["regex"], raw_text)[0]
        value_rep = value.replace(".", "").replace(",", ".")
        value_last = round(float(value_rep), 2)

        print(
            f"{decor}\n\tCompared to {types[typ]['name']}\nThe value of it, right now: ₺ {value_last}\n\t\tYou may have {round(amount/(value_last), 4)}")


def btc_try():
    # dollar
    exchangeURL = "https://kur.doviz.com" + types["dollar"]["path"]
    r = get(exchangeURL)
    soup = BeautifulSoup(r.content, "html.parser")
    marketSumForex = soup.find_all("div", {"class": "market-data"})
    divs = soup.find_all(types["dollar"]["tag"], {types["dollar"]["class"]})
    all_texts = divs[-1].text
    raw_text = all_texts.replace("\n", "")
    value = re.findall(types["dollar"]["regex"], raw_text)[0]
    value_rep = value.replace(".", "").replace(",", ".")
    value_last_dollar = round(float(value_rep), 2)

    # bitcoin
    
    exchangeURL = "https://kur.doviz.com" + types_2["bitcoin"]["path"]
    r = get(exchangeURL)
    soup = BeautifulSoup(r.content, "html.parser")
    marketSumForex = soup.find_all("div", {"class": "market-data"})
    divs = soup.find_all(types_2["bitcoin"]["tag"], {
                         types_2["bitcoin"]["class"]})
    all_texts = divs[-1].text
    raw_text = all_texts.replace("\n", "")
    value = re.findall(types_2["bitcoin"]["regex"], raw_text)[-1]
    value_rep = value.replace(".", "").replace(",", ".")
    value_last_btc = round(float(value_rep), 2)

    btc_try = value_last_dollar * value_last_btc
    print(
        f"{decor}\n\tCompared to {types_2['bitcoin']['name']}\n\t\tYou may have {round(amount/(btc_try), 8)}")


if __name__ == '__main__':
    while True:
        decor = ("*"*50)
        msg = "Welcome to Instant Exchange Convertor".center(50, "*")
        exe = input(
            f"\n{decor}\n{msg}\n{decor}\nFor starting, type 's'\nFor quitting, type 'q'\nWhat\'s your choice: ")

        if exe == "s" or exe == "S":
            amount = round(
                float(input(f"\nPlease enter an amount (TRY) to invest in: ")), 2)
            print(
                f"\nThe exact moment right now is; {time}\nYou have '₺ {amount}' for investing.\nAccording to the instant situation of the markets;")

            exc_try()
            btc_try()
            sleep(60)
            print("\nRestarting in 10 secs...")
            sleep(10)

        elif exe == "q" or exe == "Q":
            print("\nProgram is shutting down... Open it again whenever you need to.")
            sleep(10)
            break

        else:
            print("Type error! Please try again with correct letter;")
            exe
