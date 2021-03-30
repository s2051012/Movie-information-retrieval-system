# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from exts import db


class Actor(db.Model):
    __tablename__ = 'actors'

    count = db.Column(db.Integer, primary_key=True)
    actor_name = db.Column(db.Text, nullable=False, info='演员名')
    pos = db.Column(db.Text, nullable=False, info='演员位置')
    film_id = db.Column(db.ForeignKey('film.film_id', ondelete='CASCADE'), nullable=False, index=True, info='参演电影id')

    film = db.relationship('Film', primaryjoin='Actor.film_id == Film.film_id', backref='actors')


class Country(db.Model):
    __tablename__ = 'countries'

    count = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.Text, nullable=False, info='电影生产国')
    film_id = db.Column(db.ForeignKey('film.film_id', ondelete='CASCADE'), nullable=False, index=True, info='电影id')

    film = db.relationship('Film', primaryjoin='Country.film_id == Film.film_id', backref='countries')


class Director(db.Model):
    __tablename__ = 'directors'

    count = db.Column(db.Integer, primary_key=True)
    director_name = db.Column(db.Text, nullable=False, info='导演姓名')
    film_id = db.Column(db.ForeignKey('film.film_id', ondelete='CASCADE'), nullable=False, index=True, info='导演电影id')

    film = db.relationship('Film', primaryjoin='Director.film_id == Film.film_id', backref='directors')


class Film(db.Model):
    __tablename__ = 'film'

    film_id = db.Column(db.String(40), primary_key=True, info='电影id')
    actor_string = db.Column(db.Text, nullable=False, info='电影演员')
    name = db.Column(db.Text, info='电影名')
    other_name = db.Column(db.Text, info='电影别名')
    description = db.Column(db.Text, info='电影描述')
    keywords = db.Column(db.Text, info='电影关键字')
    storyline = db.Column(db.Text, info='电影故事情节简述')
    storyline_writer = db.Column(db.Text, info='故事情节作者')
    storyline_writer_hyperlink = db.Column(db.Text, info='故事情节作者超链接')
    image = db.Column(db.Text, info='电影海报链接')
    photos = db.Column(db.Text, info='电影节选海报链接')
    time = db.Column(db.Text, info='电影时长')
    date = db.Column(db.Text, info='电影上映时间')
    imdb_url = db.Column(db.Text, info='imdb的链接')
    rating_count = db.Column(db.Integer)
    rating_value = db.Column(db.Text)
    more_reviews_url = db.Column(db.Text)
    gross = db.Column(db.Text, info='票房')


class Genre(db.Model):
    __tablename__ = 'genres'

    count = db.Column(db.Integer, primary_key=True)
    genres = db.Column(db.Text, nullable=False, info='电影类别')
    film_id = db.Column(db.ForeignKey('film.film_id', ondelete='CASCADE'), nullable=False, index=True, info='电影id')

    film = db.relationship('Film', primaryjoin='Genre.film_id == Film.film_id', backref='genres')


class InvertActor(db.Model):
    __tablename__ = 'invert_actor'

    count = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.ForeignKey('film.film_id', ondelete='CASCADE'), nullable=False, index=True, info='参演电影id')
    actor_token = db.Column(db.Text, nullable=False)
    pos = db.Column(db.Text, nullable=False)

    film = db.relationship('Film', primaryjoin='InvertActor.film_id == Film.film_id', backref='invert_actors')


class InvertDe(db.Model):
    __tablename__ = 'invert_des'

    count = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.ForeignKey('film.film_id', ondelete='CASCADE'), nullable=False, index=True, info='参演电影id')
    des_token = db.Column(db.Text, nullable=False)
    pos = db.Column(db.Text, nullable=False)

    film = db.relationship('Film', primaryjoin='InvertDe.film_id == Film.film_id', backref='invert_des')


class InvertDirector(db.Model):
    __tablename__ = 'invert_director'

    count = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.ForeignKey('film.film_id', ondelete='CASCADE'), nullable=False, index=True, info='参演电影id')
    director_token = db.Column(db.Text, nullable=False)
    pos = db.Column(db.Text, nullable=False)

    film = db.relationship('Film', primaryjoin='InvertDirector.film_id == Film.film_id', backref='invert_directors')


class InvertName(db.Model):
    __tablename__ = 'invert_name'

    count = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.ForeignKey('film.film_id', ondelete='CASCADE'), nullable=False, index=True, info='参演电影id')
    name_token = db.Column(db.Text, nullable=False)
    pos = db.Column(db.Text, nullable=False)

    film = db.relationship('Film', primaryjoin='InvertName.film_id == Film.film_id', backref='invert_names')


class InvertOtherName(db.Model):
    __tablename__ = 'invert_other_name'

    count = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.ForeignKey('film.film_id', ondelete='CASCADE'), nullable=False, index=True, info='参演电影id')
    other_name_token = db.Column(db.Text, nullable=False)
    pos = db.Column(db.Text, nullable=False)

    film = db.relationship('Film', primaryjoin='InvertOtherName.film_id == Film.film_id', backref='invert_other_names')


class Language(db.Model):
    __tablename__ = 'languages'

    count = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.Text, nullable=False, info='电影语言')
    film_id = db.Column(db.ForeignKey('film.film_id', ondelete='CASCADE'), nullable=False, index=True, info='电影id')

    film = db.relationship('Film', primaryjoin='Language.film_id == Film.film_id', backref='languages')


class Production(db.Model):
    __tablename__ = 'productions'

    count = db.Column(db.Integer, primary_key=True)
    production_name = db.Column(db.Text, nullable=False, info='制片厂')
    film_id = db.Column(db.ForeignKey('film.film_id', ondelete='CASCADE'), nullable=False, index=True, info='制片id')

    film = db.relationship('Film', primaryjoin='Production.film_id == Film.film_id', backref='productions')


class Student(db.Model):
    __tablename__ = 'students'

    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))


class UserMovie(db.Model):
    __tablename__ = 'user_movie'

    count = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(40), nullable=False, info='用户id')
    film_id = db.Column(db.ForeignKey('film.film_id', ondelete='CASCADE'), nullable=False, index=True, info='用户喜爱电影id')

    film = db.relationship('Film', primaryjoin='UserMovie.film_id == Film.film_id', backref='user_movies')
