import os
import requests
import time
import json
from bs4 import BeautifulSoup
from ViewModel.utils import preprocessing

search_url = 'https://www.imdb.com/find?q={}&s=tt&ref_=fn_al_tt_mr'


def get_page_html(query):
    """
    :param query: str. Note we only support search by film.
    :return: html
    """
    query = '%20'.join(preprocessing(query))
    url = search_url.format(query)
    try:
        homepage_response = requests.get(url)
        homepage_response.raise_for_status()
        homepage_response.encoding = homepage_response.apparent_encoding
        return homepage_response.text
    except:
        return None


def decode_html(http_response):
    """
    :param http_response: http response
    :return: list of films
    """
    soup = BeautifulSoup(http_response, 'lxml')
    result_list = soup.find_all('tr', class_='findResult odd')
    film_id_list = []
    for result in result_list:
        attribute = result.a['href']
        attribute = attribute.replace('title', '').replace('/', '')
        film_id_list.append(attribute)
    return film_id_list


def search_batch(query_list):
    """
    :param query_list: Given a list of query
    :return: return a list of list
    """
    dict_of_list = dict()
    for i, query in enumerate(query_list):
        result_list = decode_html(get_page_html(query))
        dict_of_list[query] = result_list
        time.sleep(10)
    return dict_of_list


if __name__ == '__main__':
    query_list = [
        'star war',
        'harry potter',
    ]
    dict_of_list = search_batch(query_list)
    for k, v in dict_of_list.items():
        print(k, v)
    file = open(os.path.join(os.path.curdir, 'eval.json'), 'w')
    json.dump(dict_of_list, file, indent=1)
    file.close()
