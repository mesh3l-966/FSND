import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, DateTime, Table
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date
#from flask import abort

from sqlalchemy.orm import relationship

#database_name = "capstone"
#database_path = "postgresql://{}/{}".format('postgres:laug999@localhost:5432', database_name)
database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Show
'''

shows_table = Table('shows', db.metadata,
                    Column('actors_id', Integer, ForeignKey('actors.id'), nullable=False),
                    Column('movies_id', Integer, ForeignKey('movies.id'), nullable=False)
                    )


'''
Movie

'''
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(DateTime)
    #actors = relationship('Actor', backref='movies', lazy=True)
    actors = relationship("Actor", secondary=shows_table, back_populates="movies")

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date


    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

'''
Actor

'''
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    birth_date = Column(DateTime)
    #movies = relationship('Movie', backref='actors', lazy=True)
    movies = relationship("Movie", secondary=shows_table, back_populates="actors")

    def __init__(self, name, gender, birth_date):
        self.name = name
        self.gender = gender
        self.birth_date = birth_date

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'birth_date': self.birth_date
        }

"""
class Show(db.Model):
    __tablename__ = 'shows'

    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey('actors.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
"""