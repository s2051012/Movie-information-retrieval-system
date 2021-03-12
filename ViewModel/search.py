import re
from ViewModel import utils
from Model import db_search_interface as db


class Searcher():
    def __init__(self):
        self.GENRE = ['comedy', 'sci-fi', 'horror', 'romance', 'action', 'thriller', 'drama', 'mystery', 'crime',
                      'animation', 'adventure', 'fantasy']

    def boolean_search_by_genre(self, genres: list, unfiltered_films: list):
        # 给我一个你想要的Genre列表，一个未过滤的电影表(list of dict)，返回一个过滤后的列表
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

    def search_by_id(self, id: str):
        return utils.film_convert_list_to_dict(db.film_information(id))
        

s = Searcher()
for i, k in s.search_by_id('tt0004288').items():
    print(i, k)
