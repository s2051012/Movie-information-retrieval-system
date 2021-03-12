import re


def preprocessing(text: str):
    """
    :param text: a piece of text
    :return: Lowercase. Replace all non-English token to <space>. Then, divided by <space>.
    """
    text = text.lower()  # lowercase
    # text = re.sub('[^a-z0-9 ]', ' ', text)  # replace to <space>
    words_list = re.split("[,.-: ]+", text)  # get words list
    words_list = [word for word in words_list if word != '']  # remove empty str
    return words_list

def film_convert_list_to_dict(film_info: list):
    """
    :param film_info: a list contains [movie id(str), actors(str),
    :return:
    """
    pass
