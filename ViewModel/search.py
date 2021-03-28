import os
from autocorrect import Speller
from nltk.corpus import wordnet as wn
from ViewModel import utils
from Model import db_search_interface as db
from collections import OrderedDict


class Searcher():
    """
    Interface:
    boolean_search_by_genre 按照给定genre进行过滤
    search_by_id 拿到一个电影的全部信息
    default_search 默认搜索
    search_by_film_name 按电影名检索
    search_by_actor 按演员检索
    search_by_director 按导演检索
    search_by_description 按描述检索
    """

    def __init__(self):
        self.GENRE = ['comedy', 'sci-fi', 'horror', 'romance', 'action', 'thriller', 'drama', 'mystery', 'crime',
                      'animation', 'adventure', 'fantasy']
        self.stop_words = set()
        file = open(os.path.join(utils.__file__, '..', 'englishST.txt'))
        for line in file:
            self.stop_words.add(line.strip())
        file.close()
        self.spell_checker = Speller(lang='en', fast=True)

    def boolean_search_by_genre(self, genres: list, unfiltered_films: list):
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

    def search_by_id(self, id: str):
        """
        :param id: film id
        :return: a dictionary represents information of this film
        """
        return utils.film_convert_list_to_dict(db.film_information(id))

    def default_search(self, query: str):
        """
        :param query: query text
        :return: an OrderedDict contains (film_id: its score)
        """
        score = self.search_by_film_name(query)
        score = utils.merge_two_dict(score, self.search_by_actor(query))
        score = utils.merge_two_dict(score, self.search_by_director(query))
        return OrderedDict(sorted(score.items(), key=lambda t: t[1], reverse=True))

    def search_by_film_name(self, query: str):
        """
        :param query: query text
        :return: an OrderedDict contains (film_id: its score)
        """
        token_list = utils.preprocessing(query)
        token_list = [self.spell_checker(token) for token in token_list]  # spell correction
        film_score_name = self.proximity_search(token_list, 'invert_name', max_diff=3)
        film_score_other_name = self.proximity_search(token_list, 'invert_other_name', max_diff=3)

        score = utils.merge_two_dict(film_score_name, film_score_other_name)
        score = OrderedDict(sorted(score.items(), key=lambda t: t[1], reverse=True))
        return score

    def search_by_actor(self, query: str):
        """
        :param query: query text
        :return: an OrderedDict contains (film_id: its score)
        """
        token_list = utils.preprocessing(query)
        film_score_actor = self.proximity_search(token_list, 'invert_actor', max_diff=2)

        score = OrderedDict(sorted(film_score_actor.items(), key=lambda t: t[1], reverse=True))
        return score

    def search_by_director(self, query: str):
        """
        :param query: query text
        :return: an OrderedDict contains (film_id: its score)
        """
        token_list = utils.preprocessing(query)
        film_score_director = self.proximity_search(token_list, 'invert_director', max_diff=2)

        score = OrderedDict(sorted(film_score_director.items(), key=lambda t: t[1], reverse=True))
        return score

    def search_by_description(self, query: str):
        """
        :param query: query text
        :return: an OrderedDict contains (film_id: its score)
        """
        token_list = utils.preprocessing(query, stop=self.stop_words)
        tf_idf = dict()
        for token in token_list:
            temp = self.calculate_description_tfidf(token)
            synonym = self.get_synonym(token)  # query expansion
            if synonym is not None:
                temp = utils.merge_two_dict(temp, self.calculate_description_tfidf(synonym))
            temp = sorted(temp.items(), key=lambda t: t[1], reverse=True)
            tf_idf = utils.merge_two_dict(tf_idf, dict(temp[:100]))  # beam search top-100

        return OrderedDict(sorted(tf_idf.items(), key=lambda t: t[1], reverse=True))

    # ---------------------------------------------------------------------------------------------------
    # The following functions are not suggested to be called. They are not interface functions!!!
    # ---------------------------------------------------------------------------------------------------

    def proximity_search(self, token_list: list, which_table: str, max_diff=3, weight=6.0, decay=1.0):
        """
        :param token_list: list of token
        :param which_table: invert_name/invert_other_name/invert_actor/invert_director/invert_des
        :param max_diff: max word distance in calculation (should smaller than 3)
        :param weight: initial score for word distance = 1
        :param decay: word distance decay, word distance + 1, score ** decay
        :return: a set of movie id
        """
        if len(token_list) == 1:  # only one token case
            temp = sorted(self.one_token_search(token_list[0], which_table).items(), key=lambda t: t[1], reverse=True)
            return OrderedDict(temp[:30])
        token_pairs = []
        for i, token in enumerate(token_list):
            if i + 1 != len(token_list):
                token_pairs.append((token, token_list[i + 1]))

        candidate_dict = dict()
        for i, (t1, t2) in enumerate(token_pairs):
            list1 = db.invert_data(which_table, t1)
            list2 = db.invert_data(which_table, t2)
            if i == 0:
                candidate_dict = self.search_candidate_document(list1, list2, max_diff, weight, decay)
            else:
                can_dict = self.search_candidate_document(list1, list2, max_diff, weight, decay)
                candidate_dict = utils.merge_two_dict(candidate_dict, can_dict)

        # robust to wrong vocab
        for i, token in enumerate(token_list):
            if i + 2 >= len(token_list):
                break
            list1 = db.invert_data(which_table, token)
            list2 = db.invert_data(which_table, token_list[i + 2])
            can_dict = self.search_candidate_document(list1, list2, max_diff, weight, decay, skip=False)
            candidate_dict = utils.merge_two_dict(candidate_dict, can_dict)
        return candidate_dict

    def search_candidate_document(self, list1, list2, max_diff=3, weight=6.0, decay=1.0, skip=False):
        """
        :param list1: list/tuple of tuples (primary key, document id, token, position)
        :param list2: list/tuple of tuples (primary key, document id, token, position)
        :param max_diff: max word distance we count
        :param weight: initial score for word distance = 1
        :param decay: word distance decay, word distance + 1, score ** decay
        :return: list of candidate documents
        """
        candidate_dict = dict()
        pointer1 = 0
        pointer2 = 0
        while pointer1 < len(list1) and pointer2 < len(list2):
            document_id1 = list1[pointer1][1]
            document_id2 = list2[pointer2][1]

            if document_id1 == document_id2:
                diff = abs(int(list1[pointer1][3]) - int(list2[pointer2][3]))
                if skip:
                    if diff == 2:
                        candidate_dict = utils.safe_add(candidate_dict, document_id1, weight * decay)
                elif diff == 1 and max_diff >= 1:
                    candidate_dict = utils.safe_add(candidate_dict, document_id1, weight)
                elif diff == 2 and max_diff >= 2:
                    candidate_dict = utils.safe_add(candidate_dict, document_id1, weight ** decay)
                elif diff == 3 and max_diff >= 3:
                    candidate_dict = utils.safe_add(candidate_dict, document_id1, weight ** decay ** decay)
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

        return candidate_dict

    def calculate_description_tfidf(self, token: str):
        token_inverted_index = db.invert_data('invert_des', token)
        tf = dict()  # term frequency, (document id: tf)
        df = 0  # document frequency
        for (sql_primary_key, film_id, token, position) in token_inverted_index:
            if film_id not in tf.keys():
                df += 1
                tf[film_id] = 1
            else:
                tf[film_id] += 1

        tf_idf = dict()
        for film_id in tf:
            tf_idf[film_id] = utils.tf_idf(tf[film_id], df)
        return tf_idf

    def one_token_search(self, token: str, type: str):  # give higher score for token at first position, plus TF-IDF
        score = dict()
        token_inverted_index = db.invert_data(type, token)
        tf = dict()  # term frequency, (document id: tf)
        df = 0  # document frequency
        for (sql_primary_key, film_id, token, position) in token_inverted_index:
            if film_id not in tf.keys():
                df += 1
                tf[film_id] = 1
            else:
                tf[film_id] += 1
            if int(position) == 1:
                score = utils.safe_add(score, film_id, 5.)

        score2 = dict()
        for film_id in tf:
            score2[film_id] = utils.tf_idf(tf[film_id], df)
        return utils.merge_two_dict(score, score2)

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

    def get_synonym(self, token):
        # s = Searcher()
        # print(s.get_synonym('girl'))
        syn_set = wn.synsets(token)[0]
        for lemma in syn_set.lemma_names():
            if lemma != token:
                return lemma
        return token
