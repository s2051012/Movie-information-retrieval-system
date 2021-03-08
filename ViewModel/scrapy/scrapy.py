import requests
import random
import re
import time
import logging
import json
import os
import argparse
from bs4 import BeautifulSoup

movie_homepage = 'https://www.imdb.com/title/{}/?pf_rd_m=1'
reviews_page = 'https://www.imdb.com/title/{}/reviews?ref_=tt_urv'
user_reviews_page_10star = 'https://www.imdb.com/user/{}/reviews?sort=userRating&dir=desc&ratingFilter=10'
user_reviews_page_9star = 'https://www.imdb.com/user/{}/reviews?sort=userRating&dir=desc&ratingFilter=9'
user_reviews_page_8star = 'https://www.imdb.com/user/{}/reviews?sort=userRating&dir=desc&ratingFilter=8'
genre_page = 'https://www.imdb.com/search/title/?genres={}&start={}&ref_=adv_nxt'
genre_page_after_10000 = 'https://www.imdb.com/search/title/?genres={}&after={}&ref_=adv_nxt'
original = 'https://www.imdb.com{}'

header = {'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7'}


def http_get_by_movie_id(mid):
    """
    :param mid: movie id, should be a string with 'tt' and 7-8 digits following. For example: tt1234567
    :return: http response content. If the http status code not equals to 200, it would return None
    """
    homepage_url = movie_homepage.format(mid)
    try:
        homepage_response = requests.get(homepage_url, headers=header)
        homepage_response.raise_for_status()
        homepage_response.encoding = homepage_response.apparent_encoding
        return homepage_response.text
    except:
        return None


def http_get_by_url(url):
    """
    :param url: url, should be a string.
    :return: http response content. If the http status code not equals to 200, it would return None
    """
    try:
        homepage_response = requests.get(url, headers=header)
        homepage_response.raise_for_status()
        homepage_response.encoding = homepage_response.apparent_encoding
        return homepage_response.text
    except:
        return None


def encode_to_json(mid, homepage_response):
    """
    :param mid: movie id, should be a string with 'tt' and seven digits following. For example: tt1234567
    :param homepage_response: http response from http_get_by_movie_id(mid). Dont accept None value
    :return: encoded dict
    """
    homepage_soup = BeautifulSoup(homepage_response, 'lxml')
    homepage_dict = json.loads(homepage_soup.find('script', type="application/ld+json").string)
    encoded = dict()
    encoded['id'] = mid
    encoded['name'] = homepage_dict['name']
    if 'director' not in homepage_dict:
        encoded['director'] = ''
    elif homepage_dict['director'].__class__.__name__ == 'list':
        encoded['director'] = homepage_dict['director'][0]['name']
    else:
        encoded['director'] = homepage_dict['director']['name']
    encoded['genres'] = homepage_dict['genre'] if 'genre' in homepage_dict else []
    encoded['actor'] = [dict['name'] for dict in homepage_dict['actor']] if 'actor' in homepage_dict else []
    encoded['date'] = homepage_dict['datePublished'] if 'datePublished' in homepage_dict else ''
    encoded['imdb_url'] = movie_homepage.format(mid)
    encoded['description'] = homepage_dict['description'].strip() if 'description' in homepage_dict else ''
    encoded['image'] = homepage_dict['image'] if 'image' in homepage_dict else ''
    encoded['keywords'] = homepage_dict['keywords'].split(',') if 'keywords' in homepage_dict else []
    encoded['rating_count'] = homepage_dict['aggregateRating'][
        'ratingCount'] if 'aggregateRating' in homepage_dict else 0
    encoded['rating_value'] = homepage_dict['aggregateRating'][
        'ratingValue'] if 'aggregateRating' in homepage_dict else '0.0'
    encoded['more_reviews_url'] = reviews_page.format(mid)
    if homepage_soup.find('div', class_='inline canwrap') is not None:
        storyline_tag = homepage_soup.find('div', class_='inline canwrap').find('p')
        if storyline_tag.find('em', class_='nobr') is not None:
            storyline_writer_tag = storyline_tag.find('em', class_='nobr').find('a')
        else:
            storyline_writer_tag = None
    else:
        storyline_tag = None
        storyline_writer_tag = None
    if storyline_tag is not None:
        if storyline_tag.find('span') is not None and storyline_tag.find('span').string is not None:
            encoded['storyline'] = storyline_tag.find('span').string.strip()
        else:
            encoded['storyline'] = ''
    else:
        encoded['storyline'] = ''
    encoded['storylineWriter'] = storyline_writer_tag.string if storyline_writer_tag is not None else ''
    encoded['storylineWriterHyperlink'] = original.format(
        storyline_writer_tag['href']) if storyline_writer_tag is not None else ''
    encoded['time'] = homepage_soup.find('time').string.strip() if homepage_soup.find('time') is not None else ''
    production_tags = homepage_soup.find_all('a', href=re.compile('/company/'))
    encoded['productions'] = [tag.string.strip() for tag in production_tags]
    if homepage_soup.find('div', class_='mediastrip') is not None:
        photos_tags = homepage_soup.find('div', class_='mediastrip').find_all('a')
    else:
        photos_tags = None
    country_tag = homepage_soup.find('a', href=re.compile('country'))
    encoded['country'] = country_tag.string if country_tag is not None else ''
    language_tags = homepage_soup.find_all('a', href=re.compile('language'))
    encoded['languages'] = [tag.string.strip() for tag in language_tags]
    other_name_tag = homepage_soup.find('a', href=re.compile('akas'))
    if other_name_tag is not None:
        other_name_tag = other_name_tag.parent
        encoded['otherName'] = other_name_tag.previous_sibling.strip()
    else:
        encoded['otherName'] = ''
    gross_candidates = homepage_soup.find_all('h4', class_='inline')
    for tag in gross_candidates:
        if tag.string == 'Cumulative Worldwide Gross:':
            encoded['gross'] = tag.next_sibling.strip()
            break
        else:
            encoded['gross'] = ''
    user_tag = homepage_soup.find('a', href=re.compile('/user/'))
    userID = user_tag['href'] if user_tag is not None else None
    if userID is not None:
        userID = userID[6:].replace('/', '')
    encoded['photos'] = [tag['href'] for tag in photos_tags] if homepage_soup is not None else []
    return encoded, userID


def random_movie_id():
    """
    :return: a random movie id
    """
    randi = str(random.randint(0, 5000000))
    return 'tt' + randi


def catch_50_movies(genre, page_num=0):
    """
    :param genre: the genre. For example: comedy, sci-fi, horror, romance, action.
    (See: https://www.imdb.com/feature/genre/?ref_=nv_ch_gr)
    :param page_num: page number (start = pages_num * 50 + 1)
    :return: a list of movie IDs
    """
    page_num = page_num * 50 + 1
    search_url = genre_page.format(genre, page_num)
    search_page = http_get_by_url(search_url)
    soup = BeautifulSoup(search_page, 'lxml')
    tags = soup.find_all('img', class_='loadlate')
    mid_list = [tag['data-tconst'] for tag in tags]
    return mid_list


def catch_50_movies_by_hash(genre, page_hash):
    search_url = genre_page_after_10000.format(genre, page_hash)
    search_page = http_get_by_url(search_url)
    soup = BeautifulSoup(search_page, 'lxml')
    tags = soup.find_all('img', class_='loadlate')
    mid_list = [tag['data-tconst'] for tag in tags]
    query = '/search/title/\?genres={}&after'.format(genre)
    next_page_candidate = soup.find('a', href=re.compile(query), text=re.compile('Next'))['href']
    removal = '/search/title/?genres={}&after='.format(genre)
    next_page = next_page_candidate.replace(removal, '')
    return mid_list, next_page


def catch_user_favorites(uid):
    """
    :param uid: user id. For example: ur27443865
    catch user favorites, and write to file <user_id>.json
    """
    user_favorite_movies = []
    for page in [user_reviews_page_10star, user_reviews_page_9star, user_reviews_page_8star]:
        search_url = page.format(uid)
        search_page = http_get_by_url(search_url)
        soup = BeautifulSoup(search_page, 'lxml')
        tags = soup.find_all('div', class_='uc-add-wl-ribbon uc-add-wl--not-in-wl uc-add-wl')
        user_favorite_movies += [tag['data-title-id'] for tag in tags]
    data_dir = os.path.join(os.getcwd(), 'user')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    data_dir = os.path.join(data_dir, uid + '.json')
    with open(data_dir, 'w') as file:
        file.write(json.dumps(user_favorite_movies, indent=1))


def main_loop(genre, start_pages=0):  # fetch 1000 movies every time
    data_dir = os.path.join(os.getcwd(), 'json')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    data_dir = os.path.join(data_dir, genre)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    for page_num in range(start_pages, start_pages + 20):
        mid_list = catch_50_movies(genre, page_num)
        for mid in mid_list:
            time.sleep(10)
            http_response = http_get_by_movie_id(mid)
            try:
                encoded, uid = encode_to_json(mid, http_response)
                with open(os.path.join(data_dir, mid + '.json'), 'w') as file:
                    file.write(json.dumps(encoded, indent=1))
                logging.info('Page {}, Movie \"{}\" Write to file {}.json.'.format(page_num, encoded['name'], mid))
                if uid is not None:
                    try:
                        catch_user_favorites(uid)
                        logging.info('User {} write to file {}.json'.format(uid, uid))
                    except Exception as e:
                        logging.info('User {} format wrong. Skip'.format(uid))
                        logging.warning(e)
            except Exception as e:
                logging.info('Page {}, MID \"{}\" HTTP format wrong. Skip.'.format(page_num, mid))
                logging.warning(e)


def main_loop_after_10000(genre, max_iter=20):  # after 10000 movies. Please keep "page.json" in the same directory!
    data_dir = os.path.join(os.getcwd(), 'json')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    data_dir = os.path.join(data_dir, genre)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    json_data = os.path.join(os.path.curdir, genre + '-pages-hash')
    if not os.path.isfile(json_data):
        with open(json_data, 'w') as file0:
            file0.write('WzMwNTAzLCJ0dDE4NjEyMjUiLDEwMDAwXQ%3D%3D\n')
    file1 = open(json_data, 'r')
    page_hash = file1.readlines()[-1].strip()  # load data
    file1.close()

    with open(json_data, 'a') as file2:
        for iter in range(max_iter):
            mid_list, next_page_hash = catch_50_movies_by_hash(genre, page_hash)
            for mid in mid_list:
                time.sleep(10)
                http_response = http_get_by_movie_id(mid)
                try:
                    encoded, uid = encode_to_json(mid, http_response)
                    with open(os.path.join(data_dir, mid + '.json'), 'w') as file:
                        file.write(json.dumps(encoded, indent=1))
                    logging.info('Iter {}, Movie \"{}\" Write to file {}.json.'.format(iter, encoded['name'], mid))
                    if uid is not None:
                        try:
                            catch_user_favorites(uid)
                            logging.info('User {} write to file {}.json'.format(uid, uid))
                        except Exception as e:
                            logging.info('User {} format wrong. Skip'.format(uid))
                            logging.warning(e)
                except Exception as e:
                    logging.info('Page {}, Iter{}, MID \"{}\" HTTP format wrong. Skip.'.format(page_hash, iter, mid))
                    logging.warning(e)
            page_hash = next_page_hash
            file2.write(page_hash + '\n')
            file2.flush()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--genre', type=str, help='which genre(type) of movies. '
                                                        'See: https://www.imdb.com/feature/genre/?ref_=nv_ch_gr')
    parser.add_argument('-p', '--page', type=int, help='the page number. The scrapy will try to read all movies in'
                                                       ' this page and the next 19 pages.')
    parser.add_argument('-m', '--max-iter', type=int, default=0, help='If movies > 10000, please give this argument: '
                                                                      'How many number of pages you want to fetch. '
                                                                      'Suggested: 20')
    args = parser.parse_args()
    genre = args.genre
    GENRES = ['comedy', 'sci-fi', 'horror', 'romance', 'action', 'thriller', 'drama', 'mystery', 'crime', 'animation',
              'adventure', 'fantasy']
    assert genre in GENRES, ('Your genre input is wrong. Check if your input is in list: {}'.format(GENRES))

    if args.max_iter == 0:
        page = args.page
        main_loop(genre, page)
    else:
        main_loop_after_10000(genre, max_iter=args.max_iter)
