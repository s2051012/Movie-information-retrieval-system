from flask import Flask, request, flash, url_for, redirect, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template, Blueprint
from config import Config
from exts import db
from model import Student, Film, Genre, Country, Actor, Director, Language, Production, Country, Genre
import math
import pymysql
from ViewModel.search import Searcher

# from Model import db_search_interface
app = Flask(__name__, template_folder='./templates', static_folder='./templates/static')
app.config.from_object(Config)
db.init_app(app)
db.create_all(app=app)
p = 0

import nltk


# nltk.download()

@app.route('/')
def homepage_films():
    ranking_films = Film.query.order_by(Film.rating_value.desc()).limit(24)
    return render_template('homepage.html', ranking_films=ranking_films)
    # return render_template('test.html')


@app.route('/searchfilmsDefault', methods=['POST', 'GET'])
def searched_films_default():
    if request.method == 'POST':
        search_keywords = request.form
        search_str = ''
        for value in search_keywords.values():
            search_str += value
        s = Searcher()
        search_results = s.default_search(search_str).keys()
        print(search_results)
        film_info = []
        for id in search_results:
            film_info.append(s.search_by_id(id))
            # film_info.append(db_search_interface.film_information(id))
        for film in film_info:
            if len(film[-3]) != 1:
                film[-3] = " / ".join(film[-3])
            if len(film[-6]) != 1:
                film[-6] = " / ".join(film[-6])
            if len(film[5]) == 1:
                film[5] = 'No Records'
            else:
                film[5] = " / ".join(film[5])
        return render_template('search results.html', film_info=film_info)


@app.route('/searchfilmsName', methods=['POST', 'GET'])
def searched_films_name():
    if request.method == 'POST':
        search_keywords = request.form
        search_str = ''
        for value in search_keywords.values():
            search_str += value
        s = Searcher()
        search_results = s.search_by_film_name(search_str).keys()
        film_info = []
        for id in search_results:
            film_info.append(s.search_by_id(id))
        for film in film_info:
            if len(film[-3]) != 1:
                film[-3] = " / ".join(film[-3])
            if len(film[-6]) != 1:
                film[-6] = " / ".join(film[-6])
            if len(film[5]) == 1:
                film[5] = 'No Records'
            else:
                film[5] = " / ".join(film[5])
        return render_template('search results.html', film_info=film_info)


@app.route('/searchfilmsDirector', methods=['POST', 'GET'])
def searched_films_director():
    if request.method == 'POST':
        search_keywords = request.form
        search_str = ''
        for value in search_keywords.values():
            search_str += value
        print(search_str)
        s = Searcher()
        search_results = s.search_by_director(search_str).keys()
        film_info = []
        for id in search_results:
            film_info.append(s.search_by_id(id))
        for film in film_info:
            if len(film[-3]) != 1:
                film[-3] = " / ".join(film[-3])
            if len(film[-6]) != 1:
                film[-6] = " / ".join(film[-6])
            if len(film[5]) == 1:
                film[5] = 'No Records'
            else:
                film[5] = " / ".join(film[5])
        return render_template('search results.html', film_info=film_info)


@app.route('/searchfilmsActor', methods=['POST', 'GET'])
def searched_films_actor():
    if request.method == 'POST':
        search_keywords = request.form
        search_str = ''
        for value in search_keywords.values():
            search_str += value
        print(search_str)
        s = Searcher()
        search_results = s.search_by_actor(search_str).keys()
        film_info = []
        for id in search_results:
            film_info.append(s.search_by_id(id))
        for film in film_info:
            if len(film[-3]) != 1:
                film[-3] = " / ".join(film[-3])
            if len(film[-6]) != 1:
                film[-6] = " / ".join(film[-6])
            if len(film[5]) == 1:
                film[5] = 'No Records'
            else:
                film[5] = " / ".join(film[5])
        return render_template('search results.html', film_info=film_info)


@app.route('/searchfilmsKeywords', methods=['POST', 'GET'])
def searched_films_keywords():
    if request.method == 'POST':
        search_keywords = request.form
        search_str = ''
        for value in search_keywords.values():
            search_str += value
        print(search_str)
        s = Searcher()
        search_results = s.search_by_description(search_str).keys()
        film_info = []
        for id in search_results:
            film_info.append(s.search_by_id(id))
        for film in film_info:
            print(film[-3])
            if len(film[-3]) != 1:
                film[-3] = " / ".join(film[-3])
            if len(film[-6]) != 1:
                film[-6] = " / ".join(film[-6])
            if len(film[5]) == 1:
                film[5] = 'No Records'
            else:
                film[5] = " / ".join(film[5])
        return render_template('search results.html', film_info=film_info)


@app.route('/<genre>')
def show_genre_country_films(genre):
    genre_movies = Film.query.join(Genre, Film.film_id == Genre.film_id).filter_by(genres=genre)
    countryName = 'All'
    deter_number = 0
    for i in genre_movies:
        deter_number += 1
    return render_template('genres details.html', movies=genre_movies[0:18], number=0, countryName=countryName,
                           genre=genre, deter_number=len(genre_movies[0:18]))


@app.route('/<genre>and<countryName>page<number>')
def show_nextpage(number, countryName, genre):
    p = int(number)
    if countryName == 'All':
        deter_number = 0
        genre_movies = Film.query.join(Genre, Film.film_id == Genre.film_id).filter_by(genres=genre)
        for i in genre_movies:
            deter_number += 1
        return render_template('genres details.html', movies=genre_movies[19 * p:19 * p + 18], number=p,
                               countryName=countryName, genre=genre, deter_number=len(genre_movies[19 * p:19 * p + 18]))
    else:
        deter_number = 0
        country_all_movies = (
            Film.query.join(Country, Film.film_id == Country.film_id).filter_by(country=countryName)).join(Genre,
                                                                                                           Film.film_id == Genre.film_id).filter_by(
            genres=genre)
        for i in country_all_movies:
            deter_number += 1
        return render_template('genres details.html', movies=country_all_movies[19 * p:19 * p + 18], number=p,
                               countryName=countryName, genre=genre,
                               deter_number=len(country_all_movies[19 * p:19 * p + 18]))


@app.route('/<genre>and<countryName>page<number>')
def show_prevpage(number, countryName, genre):
    p = int(number)
    if countryName == 'All':
        genre_movies = Film.query.join(Genre, Film.film_id == Genre.film_id).filter_by(genres=genre)
        return render_template('genres details.html', movies=genre_movies[19 * p:19 * p + 18], number=p,
                               countryName=countryName, genre=genre)
    else:
        country_all_movies = (
            Film.query.join(Country, Film.film_id == Country.film_id).filter_by(country=countryName)).join(Genre,
                                                                                                           Film.film_id == Genre.film_id).filter_by(
            genres=genre)
        return render_template('genres details.html', movies=country_all_movies[19 * p:19 * p + 18], number=p,
                               countryName=countryName, genre=genre)


@app.route('/<genre>and<countryName>')
def show_country_films(countryName, genre):
    deter_number = 0
    country_all_movies = (
        Film.query.join(Country, Film.film_id == Country.film_id).filter_by(country=countryName)).join(Genre,
                                                                                                       Film.film_id == Genre.film_id).filter_by(
        genres=genre)
    for i in country_all_movies:
        deter_number += 1
    return render_template('genres details.html', movies=country_all_movies[0:18], number=0, countryName=countryName,
                           genre=genre, deter_number=len(country_all_movies[0:18]))


@app.route('/moviedetail<film_id>')
def show_movie_detail(film_id):
    film_actors = ''
    film_genres = ''
    film_country = ''
    film_languages = ''
    film_productions = ''
    detail_film = Film.query.filter_by(film_id=film_id).first()

    genres = Genre.query.filter_by(film_id=film_id)
    for genre in genres:
        film_genres = film_genres + genre.genres + ','
    film_genres = film_genres[:-1]
    if film_genres is '':
        film_genres = 'No records'

    countrys = Country.query.filter_by(film_id=film_id)
    for country in countrys:
        film_country = film_country + country.country + ','
    film_country = film_country[:-1]
    if film_country is '':
        film_actors = 'No records'

    actors = Actor.query.filter_by(film_id=film_id)
    for actor in actors:
        film_actors = film_actors + actor.actor_name + ','
    film_actors = film_actors[:-1]
    if film_actors is '':
        film_actors = 'No records'

    film_director = Director.query.filter_by(film_id=film_id).first()

    languages = Language.query.filter_by(film_id=film_id)
    for language in languages:
        film_languages = film_languages + language.language + ','
    film_languages = film_languages[:-1]
    if film_languages is '':
        film_languages = 'No records'

    productions = Production.query.filter_by(film_id=film_id)
    for production in productions:
        film_productions = film_productions + production.production_name + ','
    film_productions = film_productions[:-1]
    if film_productions is '':
        film_productions = 'No records'

    keywods = detail_film.keywords.split('_keyword_spilt_sign_')
    film_keywords = ' / '.join(keywods)
    if film_keywords == ' / ':
        film_keywords = 'No Records'
    film_photos = detail_film.photos.split('_photo_url_spilt_sign_')
    for i in range(len(film_photos)):
        film_photos[i] = 'https://www.imdb.com' + film_photos[i]
    photo_num = len(film_photos)
    carousel_num = math.ceil(photo_num / 3)

    return render_template('movie details.html', film_id=film_id, detail_film=detail_film,
                           film_genres=film_genres, film_country=film_country, film_actors=film_actors,
                           film_director=film_director, film_languages=film_languages,
                           film_productions=film_productions,
                           film_keywords=film_keywords, film_photos=film_photos, photo_num=photo_num,
                           carousel_num=carousel_num)


if __name__ == '__main__':
    app.run()
