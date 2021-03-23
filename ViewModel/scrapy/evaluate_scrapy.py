import os
import requests
import time
import json
from bs4 import BeautifulSoup
import sys
sys.path.append("..") 
from utils import preprocessing

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
    film_query_list = [
        'Black Panther',
        'harry pottter and',
        'X-Men',
        'The Avengers',
        'Avengers: Endgame',
        'Resident Evil and',
        'Black',
        'The Wizarrd of Oz',
        'A Star Is Born',
        'A Star Born',
        'A Quiet Place',
        'The Quiet Place',
        'A Night at the Opera',
        'A Night',
        'It Happened One Night',
        'It Happened Two Night',
        'Star Wars: The Last Jedi',
        'Star',
        'The Adventures of Robin Hood',
        'Leave No Trace',
        'Leave Any Trace',
        'Spider-Man: Far From Home',
        'Spider',
        'The Invisible Man',
        'La La Land',
        'La',
        'Hell or High Water',
        'The Dark Knight',
        'The Godfather',
        'The Knight',
        'Top Hat',
        'The Maltese Falcon',
        'The Mandese Falcon',
        'Sunset Boulevard',
        'Sunset',
        'Shadow of a Doubt',
        'Shadow',
        'Call Me by Your Name',
        '12 Angry Men',
        '12',
        'Schindler',
        'Fight Club',
        'The Usual Suspects',
        'The Unusual Suspects',
        'The Lion King',
        'The Tiger King',
        'Back to the Future',
        'Shining',
        'Good Will Hunting',
        'Good Willing Hunting'
    ]

    
    film_dict_of_list = search_batch(film_query_list)
    #for k, v in film_dict_of_list.items():
        #print(k, v)
    #for k, v in actor_dict_of_list.items():
        #print(k, v)
    film_file = open(os.path.join(os.path.curdir, 'film_eval.json'), 'w')
    json.dump(film_dict_of_list, film_file, indent=1)
    film_file.close()