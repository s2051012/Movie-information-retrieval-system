import re
from ViewModel import utils


class Searcher():
    def __init__(self):
        self.GENRE = ['comedy', 'sci-fi', 'horror', 'romance', 'action', 'thriller', 'drama', 'mystery', 'crime',
                      'animation', 'adventure', 'fantasy']

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

    def proximity_search(self, query: str):
        """
        :param query: query
        :return:
        """
        query_list = utils.preprocessing(query)
        

