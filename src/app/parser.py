from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import itertools


def get_url(search_phrase, region):
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


def get_full_ref(html_obj):
    first_part_url = "https://www.avito.ru"
    second_part_url = html_obj.find('a', attrs={'class': 'iva-item-sliderLink-2hFV_'}).attrs["href"]
    return first_part_url + second_part_url


def get_name(html_obj):
    name = html_obj.find('span', attrs={'itemprop': 'name'}).text
    return name


class Parser:
    """A this class is used to get data from avito html pages"""

    headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}

    def get_number_of_proposals(self, search_phrase: str, region: str) -> int:
        """It takes two parameters (search_phrase, region)
        and returns the number of ads on the avito site for this region and this search phrase
        Parameters
        ----------
        :param search_phrase: str
            unique identifier of the pair <search phrase, region>
        :param region: int
            the number of listings at the moment
        Returns
        -------
        int
            the number of ads
        """
        url = get_url(search_phrase, region)
        req = Request(url, headers=self.headers)
        webpage = urlopen(req).read()
        page_soup = BeautifulSoup(webpage, "html.parser")

        number_of_proposals_str = page_soup.find('span', attrs={'class': 'page-title-count-1oJOc'}).text
        return str_to_int(number_of_proposals_str)

    def get_top5(self, search_phrase: str, region: str) -> dict:
        """It takes two parameters (search_phrase, region)
        and returns top 5 ads on the avito site for this search phrase in this region
        Parameters
        ----------
        :param search_phrase: str
            unique identifier of the pair <search phrase, region>
        :param region: int
            the number of listings at the moment
        Returns
        -------
        dict
             a dict of dicts like {
                                    "top_1": {"name": name, "ref": href},
                                    "top_2": {"name": name, "ref": href},
                                    ...
                                }
        """
        url = get_url(search_phrase, region)
        req = Request(url, headers=self.headers)
        webpage = urlopen(req).read()
        page_soup = BeautifulSoup(webpage, "html.parser")

        result = {}
        top_counter = itertools.count(1)
        full_html = page_soup.find_all('div', attrs={'data-marker': 'item'}, limit=5)
        for i in full_html:
            n_top = next(top_counter)
            ref = get_full_ref(i)
            name = get_name(i)
            result['top_' + str(n_top)] = {"name": name, "ref": ref}
        return result
