import re


def preprocessing(text: str):
    text = text.lower()  # lowercase
    # text = re.sub('[^a-z0-9 ]', ' ', text)  # replace to <space>
    words_list = re.split("[,.-: ]+", text)  # get words list
    words_list = [word for word in words_list if word != '']  # remove empty str
    return words_list
