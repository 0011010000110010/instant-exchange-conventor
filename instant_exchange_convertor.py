import re
from requests import get
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup

now = datetime.now()
time = datetime.strftime(now, "\n%d-%B-%Y\t%H:%M:%S:%f\n")

decor = ("*"*50)
msg = "Welcome to Instant Exchange Convertor".center(50, "*")
amount = round(float(input(
    f"\n{decor}\n{msg}\n{decor}\nPlease enter an amount (TRY) to invest in: ")), 2)
print(
    f"\nThe exact moment right now is; {time}\nYou have '₺ {amount}' for investing.\nAccording to the instant situation of the markets;")

types = {
    "dollar": {
        "name": "DOLAR",
        "path": "/serbest-piyasa/amerikan-dolari",
        "tag": "div",
        "class": "market-data",
        "regex": "DOLAR(\S+)"
    },
    "bitcoin": {
        "name": "BITCOIN",
        "path": "/kripto-paralar/bitcoin",
        "tag": "ul",
        "class": "piyasa-ozeti",
        "regex": "Bitcoin\s+%\s-?[\d,]+\s+\$([\d\.,]+)"
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
        f"{decor}\n\tCompared to {types[typ]['name']}\n\t\tYou may have {round(amount/(value_last), 4)}")

sleep(60)
print("\nProgram is shutting down... Open it again whenever you need to.")
sleep(10)
