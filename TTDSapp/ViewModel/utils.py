import re
import math


def preprocessing(text: str, stop=None):
    """
    :param text: a piece of text
    :param stop: if remove stop words, please give a set of stop words
    :return: Lowercase. Replace all non-English token to <space>. Then, divided by <space>.
    """
    text = text.lower()  # lowercase
    # text = re.sub('[^a-z0-9 ]', ' ', text)  # replace to <space>
    words_list = re.split("[,.-: ]+", text)  # get words list
    words_list = [word for word in words_list if word != '']  # remove empty str
    if stop is not None:
        words_list = [word for word in words_list if word not in stop]
    return words_list


def safe_add(a_dict: dict, key: str, value: float):
    """
    :param a_dict: a dict
    :param key: the key of dict
    :param value: add some value to the key's value
    :return: a_dict
    """
    if key in a_dict.keys():
        a_dict[key] += value
    else:
        a_dict[key] = value
    return a_dict


def merge_two_dict(a_dict: dict, b_dict: dict):
    """
    :param a_dict: dict
    :param b_dict: dict
    :return: merge two dict together. If they have the same key, sum up the two values
    """
    for key in b_dict.keys():
        a_dict = safe_add(a_dict, key, b_dict[key])
    return a_dict


def tf_idf(tf, df):
    """
    :param tf: term frequency
    :param df: document frequency
    :return: TF-IDF value
    """
    return (1 + math.log10(tf)) * math.log10(1e5 / df)


def film_convert_list_to_dict(film_info: list):
    """
    :param film_info: a list extracted from Database
    :return:
    """
    film_info_dict = {'id': film_info[0],
                      'name': film_info[2],
                      'other_name': film_info[3],
                      'description': film_info[4],
                      'keywords': film_info[5],
                      'storyline': film_info[6],
                      'storyline_writer': film_info[7],
                      'storyline_writer_hyperlink': film_info[8],
                      'image': film_info[9],
                      'photos': film_info[10],
                      'time': film_info[11],
                      'date': film_info[12],
                      'imdb_url': film_info[13],
                      'rating_count': film_info[14],
                      'rating_value': film_info[15],
                      'more_reviews_url': film_info[16],
                      'gross': film_info[17],
                      'actors': film_info[18],
                      'director': film_info[19],
                      'countries': film_info[20],
                      'genres': film_info[21],
                      'languages': film_info[22],
                      'production': film_info[23]}
    return film_info_dict
