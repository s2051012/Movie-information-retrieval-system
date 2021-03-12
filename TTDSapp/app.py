from flask import Flask, request, flash, url_for, redirect, render_template,Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template,Blueprint
from config import Config
from exts import db
from model import Student,Film,Genre,Country,Actor,Director,Language,Production,Country
import math
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
db.create_all(app=app)

p = 0
@app.route('/')
def show_films():
    # sql = 'select * from film'
    # result = db.session.execute(sql)
    all_movies = Film.query.all()
    return render_template('genres details.html',movies = all_movies[0:18],number = 0)

@app.route('/page<number>')
def show_nextpage(number):
    p = int(number)
    all_movies = Film.query.all()
    return render_template('genres details.html',movies = all_movies[18*p+1:18*(p)+1+18],number = p)

@app.route('/page<number>')
def show_prevpage(number):
    p = int(number)
    all_movies = Film.query.all()
    return render_template('genres details.html',movies = all_movies[18*(p)+1:18*(p)+1+18],number = p)

@app.route('/country/<countryName>')
def show_country_films(countryName):
    country_all_movies = Film.query.join(Country, Film.film_id == Country.film_id).filter_by(country = countryName)
    return render_template('genres details.html',movies = country_all_movies[0:18],number = 0)

@app.route('/moviedetail/<film_id>')
def show_movie_detail(film_id):
    # film_id = '\'' + film_id + '\''
    # print(film_id)
    #sql = "select * from film where film_id = '{}';".format(film_id)
    # sql = "select * from film where film_id = 'tt0000002';"
    # print(sql)
    # detail_film = db.session.execute(sql)
    # print(detail_film)
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


#
# # @app.route('/')
# # def show_all():
# #    return render_template('movie details.html')
#
# @app.route('/')
# def show_all():
#     sql = 'select * from students'
#     result = db.session.execute(sql)
#     return render_template('show_all.html', students=result)
# #
# @app.route('/new', methods=['GET', 'POST'])
# def new():
#    if request.method == 'POST':
#       if not request.form['name'] or not request.form['city'] or not request.form['addr']:
#          flash('Please enter all the fields', 'error')
#       else:
#          student = Student(name = request.form['name'], city = request.form['city'], addr = request.form['addr'], pin = request.form['pin'])
#          db.session.add(student)
#          db.session.commit()
#          flash('Record was successfully added')
#          return redirect(url_for('show_all'))
#    return render_template('new.html')



if __name__ == '__main__':
    app.run()