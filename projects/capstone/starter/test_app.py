import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
from errorhandler import *


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)
        self.errors = errors(self.app)
        self.executive_producer = os.getenv('executive_producer')
        self.casting_director = os.getenv('casting_director')
        self.casting_assistant = os.getenv('casting_assistant')

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for
    successful operation and for expected errors.
    """
    def test_get_movies_without_token(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data['message']))

    def test_get_movies(self):
        res = self.client().get('/movies',
                                headers={'Authorization':
                                         'Bearer ' + self.executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_actors_without_token(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data['message']))

    def test_get_actors(self):
        res = self.client().get('/actors',
                                headers={'Authorization':
                                         'Bearer ' + self.executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_create_movie_400(self):
        res = self.client().post('/create-movie',
                                 headers={'Authorization':
                                          'Bearer ' + self.executive_producer},
                                 json={
                                    "title": "The final fanticy",
                                    "wrong_data": "04-05-2002"
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # @unittest.skip("demonstrating skipping")
    def test_create_movie(self):
        res = self.client().post('/create-movie',
                                 headers={'Authorization':
                                          'Bearer ' + self.executive_producer},
                                 json={
                                     "title": "movie from unittest2",
                                     "release_date": "04-05-2020"
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor_400(self):
        res = self.client().post('/create-actor',
                                 headers={'Authorization':
                                          'Bearer ' + self.executive_producer},
                                 json={
                                     "name": "Jacop",
                                     "age": "45",
                                     "gender": "male"
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # @unittest.skip("demonstrating skipping")
    def test_create_actor(self):
        res = self.client().post('/create-actor',
                                 headers={'Authorization':
                                          'Bearer ' + self.executive_producer},
                                 json={
                                     "name": "Jacop",
                                     "birth_date": "04-08-1977",
                                     "gender": "male"
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_modify_movie_out_of_range(self):
        res = self.client().patch('/movies/100',
                                  headers={'Authorization':
                                           'Bearer ' + self.executive_producer},
                                  json={
                                      "title": "unittest patch",
                                      "release_date": "04-05-2010"
                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_modify_movie(self):
        quer = Movie.query.get(6)
        if quer is None:
            self.title = "for modify"
            self.release_date = "02-10-1980"
            self.movie = Movie(title=self.title, release_date=self.release_date)
            self.movie.id = 6
            self.movie.insert()
        res = self.client().patch('/movies/6',
                                  headers={'Authorization':
                                           'Bearer ' + self.executive_producer},
                                  json={
                                      "title": "unittest patch",
                                      "release_date": "04-05-2010"
                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_modify_actor_out_of_range(self):
        res = self.client().patch('/actors/100',
                                  headers={'Authorization':
                                           'Bearer ' + self.executive_producer},
                                  json={
                                      "name": "Ahmed",
                                      "birth_date": "02-10-1980",
                                      "gender": "male"
                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_modify_actor(self):
        quer = Actor.query.get(5)
        if quer is None:
            self.name = "for modify"
            self.birth_date = "02-10-1980"
            self.gender = "female"
            self.actor = Actor(name=self.name, birth_date=self.birth_date, gender=self.gender)
            self.actor.id = 5
            self.actor.insert()
        res = self.client().patch('/actors/5',
                                  headers={'Authorization':
                                           'Bearer ' + self.executive_producer},
                                  json={
                                      "name": "Ahmed",
                                      "birth_date": "02-10-1980",
                                      "gender": "male"
                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie_out_of_range(self):
        res = self.client().delete('/movies/100',
                                   headers={'Authorization':
                                            'Bearer ' + self.executive_producer}
                                   )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        quer = Movie.query.get(50)
        if quer is None:
            self.title = "for deletion"
            self.release_date = "02-10-1980"
            self.movie = Movie(title=self.title, release_date=self.release_date)
            self.movie.id = 50
            self.movie.insert()
        res = self.client().delete('/movies/50',
                                   headers={'Authorization':
                                            'Bearer ' + self.executive_producer}
                                   )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor_out_of_range(self):
        res = self.client().delete('/actors/100',
                                   headers={'Authorization':
                                            'Bearer ' + self.executive_producer}
                                   )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actor(self):
        quer = Actor.query.get(50)
        if quer is None:
            self.name = "for deletion"
            self.birth_date = "02-10-1980"
            self.gender = "female"
            self.actor = Actor(name=self.name, birth_date=self.birth_date, gender=self.gender)
            self.actor.id = 50
            self.actor.insert()
        res = self.client().delete('/actors/50',
                                   headers={'Authorization':
                                            'Bearer ' + self.executive_producer}
                                   )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    """
    Role Test:
    All tests above done with Excecutive Producer. And all success since this role has full
    control.
    The following Tests are done using casting assistant and casting director roles.
    """
    def test_get_movies_assistant(self):
        res = self.client().get('/movies',
                                headers={'Authorization':
                                         'Bearer ' + self.casting_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_movies_director(self):
        res = self.client().get('/movies',
                                headers={'Authorization':
                                         'Bearer ' + self.casting_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_actors_assistant(self):
        res = self.client().get('/actors',
                                headers={'Authorization':
                                         'Bearer ' + self.casting_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_actors_director(self):
        res = self.client().get('/actors',
                                headers={'Authorization':
                                         'Bearer ' + self.casting_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_modify_movie_assistant(self):
        quer = Movie.query.get(6)
        if quer is None:
            self.title = "for modify"
            self.release_date = "02-10-1980"
            self.movie = Movie(title=self.title, release_date=self.release_date)
            self.movie.id = 6
            self.movie.insert()
        res = self.client().patch('/movies/6',
                                  headers={'Authorization':
                                           'Bearer ' + self.casting_assistant},
                                  json={
                                      "title": "unittest patch",
                                      "release_date": "04-05-2010"
                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_modify_movie_director(self):
        quer = Movie.query.get(6)
        if quer is None:
            self.title = "for modify"
            self.release_date = "02-10-1980"
            self.movie = Movie(title=self.title, release_date=self.release_date)
            self.movie.id = 6
            self.movie.insert()
        res = self.client().patch('/movies/6',
                                  headers={'Authorization':
                                           'Bearer ' + self.casting_director},
                                  json={
                                      "title": "patched by director",
                                      "release_date": "04-05-2010"
                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_modify_actor_assistant(self):
        quer = Actor.query.get(5)
        if quer is None:
            self.name = "for modify"
            self.birth_date = "02-10-1980"
            self.gender = "female"
            self.actor = Actor(name=self.name, birth_date=self.birth_date, gender=self.gender)
            self.actor.id = 5
            self.actor.insert()
        res = self.client().patch('/actors/5',
                                  headers={'Authorization':
                                           'Bearer ' + self.casting_assistant},
                                  json={
                                      "name": "Ahmed",
                                      "birth_date": "02-10-1980",
                                      "gender": "male"
                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_modify_actor_director(self):
        quer = Actor.query.get(5)
        if quer is None:
            self.name = "for modify"
            self.birth_date = "02-10-1980"
            self.gender = "female"
            self.actor = Actor(name=self.name, birth_date=self.birth_date, gender=self.gender)
            self.actor.id = 5
            self.actor.insert()
        res = self.client().patch('/actors/5',
                                  headers={'Authorization':
                                           'Bearer ' + self.casting_director},
                                  json={
                                      "name": "Ahmed",
                                      "birth_date": "02-10-1980",
                                      "gender": "male"
                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie_assistant(self):
        quer = Movie.query.get(50)
        if quer is None:
            self.title = "for deletion"
            self.release_date = "02-10-1980"
            self.movie = Movie(title=self.title, release_date=self.release_date)
            self.movie.id = 50
            self.movie.insert()
        res = self.client().delete('/movies/50',
                                   headers={'Authorization':
                                            'Bearer ' + self.casting_assistant}
                                   )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_movie_director(self):
        quer = Movie.query.get(50)
        if quer is None:
            self.title = "for deletion"
            self.release_date = "02-10-1980"
            self.movie = Movie(title=self.title, release_date=self.release_date)
            self.movie.id = 50
            self.movie.insert()
        res = self.client().delete('/movies/50',
                                   headers={'Authorization':
                                            'Bearer ' + self.casting_director}
                                   )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_actor_assistant(self):
        quer = Actor.query.get(50)
        if quer is None:
            self.name = "for deletion"
            self.birth_date = "02-10-1980"
            self.gender = "female"
            self.actor = Actor(name=self.name, birth_date=self.birth_date, gender=self.gender)
            self.actor.id = 50
            self.actor.insert()
        res = self.client().delete('/actors/50',
                                   headers={'Authorization':
                                            'Bearer ' + self.casting_assistant}
                                   )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_actor_director(self):
        quer = Actor.query.get(50)
        if quer is None:
            self.name = "for deletion"
            self.birth_date = "02-10-1980"
            self.gender = "female"
            self.actor = Actor(name=self.name, birth_date=self.birth_date, gender=self.gender)
            self.actor.id = 50
            self.actor.insert()
        res = self.client().delete('/actors/50',
                                   headers={'Authorization':
                                            'Bearer ' + self.casting_director}
                                   )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
