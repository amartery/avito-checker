from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


import datetime


def creation_url(search_phrase, region):
    list_search_words = search_phrase.split()
    q = "+".join(list_search_words)
    url = "https://www.avito.ru/{}?q={}".format(region, q)
    return url


def str_to_int(value):
    list_str_value = value.split()
    value = "".join(list_str_value)
    try:
        value = int(value)
    except ValueError:
        print("ValueError couldn't convert str to int")
    return value


def get_number_of_proposals(search_phrase, region):
    url = creation_url(search_phrase, region)
    headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    req = Request(url, headers=headers)

    webpage = urlopen(req).read()
    page_soup = BeautifulSoup(webpage, "html.parser")
    number_of_proposals_str = page_soup.find('span', attrs={'class': 'page-title-count-1oJOc'}).text
    return str_to_int(number_of_proposals_str)


# Значение: datetime.datetime(2017, 4, 5, 0, 18, 51, 980187)
now = datetime.datetime.now()

then = datetime.datetime(2020, 11, 20)

# Кол-во времени между датами.
delta = now - then

print(delta.days)
print(delta.seconds)