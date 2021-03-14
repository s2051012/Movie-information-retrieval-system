from flask import Flask, request, flash, url_for, redirect, render_template,Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template,Blueprint
from config import Config
from exts import db
from model import Student,Film,Genre,Country,Actor,Director,Language,Production,Country,Genre
import math
import pymysql
from ViewModel.search import Searcher
from Model import db_search_interface
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
db.create_all(app=app)
p = 0

@app.route('/')
def homepage_films():
    ranking_films = Film.query.order_by(Film.rating_value.desc()).limit(24)
    return render_template('homepage.html',ranking_films = ranking_films)

@app.route('/searchresults',methods = ['POST', 'GET'])
def searched_films():
    if request.method == 'POST':
        search_keywords = request.form
        search_str = ''
        for value in search_keywords.values():
            search_str += value
        s = Searcher()
        search_results = s.search_by_film_name(search_str).keys()
        film_info = []
        for id in search_results:
            film_info.append(db_search_interface.film_information(id))
        for film in film_info:
            film[-3] = " / ".join(film[-3])
            film[-6] = " / ".join(film[-6])
            if len(film[5]) == 1:
                film[5] = 'No Records'
            else:
                film[5] = " / ".join(film[5])
        return render_template('search results.html',film_info = film_info)

@app.route('/genresfiilm')
def show_films():
    # sql = 'select * from film'
    # result = db.session.execute(sql)
    all_movies = Film.query.all()
    countryName = 'All'
    # s = Searcher()
    # score = s.search_by_director('Yimou Zhang')
    # print(score)
    # info = db_search_interface.film_information('tt0000499')
    # print(info)
    # print(111111)
    return render_template('genres details.html',movies = all_movies[0:18],number = 0,countryName = countryName)

@app.route('/<countryName>page<number>')
def show_nextpage(number,countryName):
    p = int(number)
    if countryName == 'All':
        all_movies = Film.query.all()
        return render_template('genres details.html',movies = all_movies[19*p:19*p+18],number = p,countryName = countryName)
    else:
        country_all_movies = Film.query.join(Country, Film.film_id == Country.film_id).filter_by(country=countryName)
        return render_template('genres details.html', movies=country_all_movies[19*p:19*p+18], number=p,
                               countryName=countryName)

# @app.route('/page<number>')
# def show_prevpage(number):
#     p = int(number)
#     all_movies = Film.query.all()
#     return render_template('genres details.html',movies = all_movies[18*(p)+1:18*(p)+1+18],number = p)

@app.route('/<countryName>page<number>')
def show_prevpage(number,countryName):
    p = int(number)
    if countryName == 'All':
        all_movies = Film.query.all()
        return render_template('genres details.html',movies = all_movies[19*p:19*p+18],number = p,countryName = countryName)
    else:
        country_all_movies = Film.query.join(Country, Film.film_id == Country.film_id).filter_by(country=countryName)
        return render_template('genres details.html', movies=country_all_movies[19*p:19*p+18], number=p,
                               countryName=countryName)

@app.route('/country/<countryName>')
def show_country_films(countryName):
    country_all_movies = Film.query.join(Country, Film.film_id == Country.film_id).filter_by(country = countryName)
    return render_template('genres details.html',movies = country_all_movies[0:18],number = 0, countryName = countryName)


@app.route('/moviedetail/<film_id>')
def show_movie_detail(film_id):
    film_actors = ''
    film_genres = ''
    film_country = ''
    film_languages = ''
    film_productions = ''
    detail_film = Film.query.filter_by(film_id = film_id).first()

    genres = Genre.query.filter_by(film_id = film_id)
    for genre in genres:
        film_genres = film_genres + genre.genres + ','
    film_genres = film_genres[:-1]
    if film_genres is '':
        film_genres = 'No records'

    countrys = Country.query.filter_by(film_id = film_id)
    for country in countrys:
        film_country = film_country + country.country + ','
    film_country = film_country[:-1]
    if film_country is '':
        film_actors = 'No records'

    actors = Actor.query.filter_by(film_id = film_id)
    for actor in actors:
        film_actors = film_actors + actor.actor_name +','
    film_actors = film_actors[:-1]
    if film_actors is '':
        film_actors = 'No records'

    film_director = Director.query.filter_by(film_id = film_id).first()

    languages = Language.query.filter_by(film_id = film_id)
    for language in languages:
        film_languages = film_languages + language.language +','
    film_languages = film_languages[:-1]
    if film_languages is '':
        film_languages = 'No records'

    productions = Production.query.filter_by(film_id = film_id)
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
    carousel_num = math.ceil(photo_num/3)

    print(detail_film.storyline)
    return render_template('movie details.html',film_id = film_id, detail_film = detail_film,
                           film_genres = film_genres,film_country = film_country,film_actors = film_actors,
                           film_director = film_director,film_languages = film_languages, film_productions = film_productions,
                           film_keywords = film_keywords,film_photos = film_photos,photo_num = photo_num,carousel_num = carousel_num )




if __name__ == '__main__':
    app.run()