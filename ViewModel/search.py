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

    def proximity_search(self, query: str, which_table: str, max_diff=1):
        # 邻近搜索
        """
        :param query: query
        :param which_table: invert_name/invert_other_name/invert_actor/invert_director/invert_des
        :return: a set of movie id
        """
        query_list = utils.preprocessing(query)
        token_pairs = []
        for i, token in enumerate(query_list):
            if i + 1 != len(query_list):
                token_pairs.append((token, query_list[i + 1]))

        candidate_set = set()
        for i, (t1, t2) in enumerate(token_pairs):
            list1 = db.invert_data(which_table, t1)
            list2 = db.invert_data(which_table, t2)
            if i == 0:
                candidate_set = set(self.search_candidate_document(list1, list2, max_diff))
            else:
                can_list = self.search_candidate_document(list1, list2, max_diff)
                candidate_set = set(can_list).intersection(candidate_set)
        return candidate_set

    def search_by_id(self, id: str):
        # 直接从数据库上读取电影id
        """
        :param id: film id
        :return: a dictionary represents information of this film
        """
        return utils.film_convert_list_to_dict(db.film_information(id))

    # 下面的函数都不是外部接口，不建议调用

    def search_candidate_document(self, list1, list2, max_diff=1):
        """
        :param list1: list/tuple of tuples (primary key, document id, token, position)
        :param list2: list/tuple of tuples (primary key, document id, token, position)
        :return: list of candidate documents
        """
        candidate_list = []
        pointer1 = 0
        pointer2 = 0
        while pointer1 < len(list1) or pointer2 < len(list2):
            document_id1 = list1[pointer1][1]
            document_id2 = list2[pointer2][1]

            if document_id1 == document_id2:
                position1 = list1[pointer1][3]
                position2 = list2[pointer2][3]
                if abs(int(position1) - int(position2)) <= max_diff:
                    candidate_list.append(document_id1)
            document_id1 = int(document_id1.replace('tt', ''))
            document_id2 = int(document_id2.replace('tt', ''))

            if pointer1 == len(list1) - 1 and pointer2 == len(list2) - 1:
                break
            elif pointer1 == len(list1) - 1:
                pointer2 += 1
            elif pointer2 == len(list2) - 1:
                pointer1 += 1
            elif document_id1 >= document_id2:
                pointer2 += 1
            else:
                pointer1 += 1

        return candidate_list

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
print(s.proximity_search('Murder, He Says', 'invert_name'))
