import re
from ViewModel import utils
from Model import db_search_interface as db


class Searcher():
    def __init__(self):
        self.GENRE = ['comedy', 'sci-fi', 'horror', 'romance', 'action', 'thriller', 'drama', 'mystery', 'crime',
                      'animation', 'adventure', 'fantasy']

    def boolean_search_by_genre(self, genres: list, unfiltered_films: list):
        # 给一个你想要的Genre列表，一个未过滤的电影表(list of dict)，返回一个过滤后的列表
        """
        :param genres: input a list of genre
        :param unfiltered_films: unfiltered list of dict. Each dict represents a film. (Should contain "id" as a str and
        "genres" as a list) (data type: list of dictionary)
        :return: filtered_films. Filter out films which are not in the list of genres (data type: list of dictionary)
        """
        filtered_films = []
        for genre in genres:  # robust check
            if genre not in self.GENRE:
                raise Exception('Genre not found exception, while searching by genre.')
        for film in unfiltered_films:
            for film_genre in film['genres']:
                if film_genre in genres:
                    filtered_films.append(film)
                    break
        return filtered_films

    def proximity_search(self, query: str):
        """
        :param query: query
        :return:
        """
        query_list = utils.preprocessing(query)
        a = db.invert_data('invert_name', query_list[0])

        print(a)

    def search_by_id(self, id: str):
        # 直接从数据库上读取电影id
        """
        :param id: film id
        :return: a dictionary represents information of this film
        """
        return utils.film_convert_list_to_dict(db.film_information(id))

    # 下面的函数不是外部接口，不建议调用
    def linear_merge(self, list1, list2, pointer1, pointer2, max_diff):
        """
        :param list1: list of position
        :param list2: list of position (should in the same document)
        :param pointer1: list1 pointer
        :param pointer2: list2 pointer
        :param max_diff: max token distance allowed for proximity search
        :return: if the distance between terms is less than or equal to 'diff', return True, else False.
        """
        if pointer2 == len(list2) or pointer1 == len(list1):
            return False
        if abs(list2[pointer2] - list1[pointer1]) <= max_diff and list2[pointer2] >= list1[pointer1]:
            return True
        elif list1[pointer1] >= list2[pointer2]:
            return self.linear_merge(list1, list2, pointer1, pointer2 + 1, max_diff)
        else:
            return self.linear_merge(list1, list2, pointer1 + 1, pointer2, max_diff)  # tail recursion


s = Searcher()
s.proximity_search('star war')
