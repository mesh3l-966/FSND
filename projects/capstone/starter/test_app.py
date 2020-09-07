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
        #self.database_name = "capstonetest"

        #self.database_path = "postgresql://{}/{}".format('postgres:laug999@localhost:5432', self.database_name)
        database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)
        self.errors = errors(self.app)
        self.executive_producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1mbC04UmhnLXIwZVdNZWotdXZzVyJ9.eyJpc3MiOiJodHRwczovL21lc2hhbC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkZWJmYTFhMzZlYjIwMDE5N2QyOWMxIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTk0MjgyODYsImV4cCI6MTU5OTUxNDY4NiwiYXpwIjoiZHlINmxDVGFsUnB3T2ZhWmZiUVY2MlFZeUhFVWx0TnIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.25-jXgsGi1eS5L0VuSBiMNIoRSQsP2gHQR1onNCcBPl_EpsqsmLRd1R1zIfybDWNxkl65HRbfdVrFtqHxgPRgDNKthy7vUZxcU5CXHTy-e6dKInmFX-fBIhmyrq7T9SY6lIw5wb7TvpWDe_u9G1PxxsljOSrU0eW6IgWxE2rW0vrRwSpY9THlmIvXDLBT1-sQ8yZCZE6HIRcNxI3KHMTM_i8Xs1hQixxDW_K0SDwGUUK0qlCgUa8LqdgIB96ZbII9WxIJKFd9ZFekx1db2qaUZbOurm0Lyi_wKBA1M51sw8GIjLXZWb4AmjisxBzHBV9oMsJGI0ILQY8hKtVqklpug'
        self.casting_director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1mbC04UmhnLXIwZVdNZWotdXZzVyJ9.eyJpc3MiOiJodHRwczovL21lc2hhbC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY1NTU3ZjkzOTdiNzAwMDY3NTA5NjkwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTk0Mjg3NTQsImV4cCI6MTU5OTUxNTE1NCwiYXpwIjoiZHlINmxDVGFsUnB3T2ZhWmZiUVY2MlFZeUhFVWx0TnIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.6HoZzP5r-6ghPaY0gfkuV3WIwK5N_KfuoH4FfUi2qX-Hp6_qWDJ1zSIZDxxlthrqnpZe75jiDp24tuPAFwIEugBY3OJdr3QSzPrDCp2FliYHHxmVIrb3MZd_GC0qbOuDHp7aMRI0TAfj2N72xJ_pnpIH57IQmM2Yx7vKr856-gFdnG3PwPCxzzgcD42fDVgJY1s6ZN72TyTj0r95ZrWn9MyQdF_8XX9fSVJEatAP5eKhQ_LhC0z24QNP0EwL7CI__cTUksEBu73t1u9QFmx1eNvA_zsi5rWMqp3mbGBCY7XqfqUJdzFZ4-3d-vO7nTLBNeOz32vUp_GXehwLxkdTkg"
        self.casting_assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1mbC04UmhnLXIwZVdNZWotdXZzVyJ9.eyJpc3MiOiJodHRwczovL21lc2hhbC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY1NTU3ZjkzOTdiNzAwMDY3NTA5NjkwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTk0Mjg2NTUsImV4cCI6MTU5OTUxNTA1NSwiYXpwIjoiZHlINmxDVGFsUnB3T2ZhWmZiUVY2MlFZeUhFVWx0TnIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.wjOCOai7LKE-JC5azyYye5NZt2daF0LvAkO02jAF3knPpOv5uU-nnRODghrtpHlSdqVbsyQ1IGi0ApXcnFajpOThtdAdUv8XvrGVH-5iI8L5_aQyqzKBBNBB8WJwTtxQ0CwzRST_B_I7umnXuiJv8FeCIotMM90SOMvF48tj2BdB4B47fHqDX52m4VNvmi4E-Do5JcTIK1BILqnhCeiJFCeP3v1h6snHUgpCM7YCmMIe5_h-FfuhWz66nGyCdMoplJLUc3u19dm_k6lL-4_O9jGelIvZcTsE0mUsq7G-aTZkC4tZMjtrdrAK1KkzKAkRM0d20bgACvvPmTwvbM36ag"

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
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_movies_without_token(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data['message']))

    def test_get_movies(self):
        res = self.client().get('/movies',
                                headers={'Authorization':'Bearer ' +self.executive_producer})
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
                                headers={'Authorization':'Bearer ' +self.executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_create_movie_400(self):
        res = self.client().post('/create-movie',
                                 headers={'Authorization':'Bearer ' +self.executive_producer},
                                 json={
                                     "title":"The final fanticy",
                                     "wrong_data":"04-05-2002"
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    #@unittest.skip("demonstrating skipping")
    def test_create_movie(self):
        res = self.client().post('/create-movie',
                                 headers={'Authorization':'Bearer ' +self.executive_producer},
                                 json={
                                     "title":"movie from unittest2",
                                     "release_date":"04-05-2020"
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor_400(self):
        res = self.client().post('/create-actor',
                                 headers={'Authorization':'Bearer ' +self.executive_producer},
                                 json={
                                     "name":"Jacop",
                                     "age":"45",
                                     "gender":"male"
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    #@unittest.skip("demonstrating skipping")
    def test_create_actor(self):
        res = self.client().post('/create-actor',
                                 headers={'Authorization':'Bearer ' +self.executive_producer},
                                 json={
                                     "name":"Jacop",
                                     "birth_date":"04-08-1977",
                                     "gender":"male"
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_modify_movie_out_of_range(self):
        res = self.client().patch('/movies/100',
                                  headers={'Authorization':'Bearer ' +self.executive_producer},
                                  json={
                                      "title":"unittest patch",
                                      "release_date":"04-05-2010"
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
                                  headers={'Authorization':'Bearer ' +self.executive_producer},
                                  json={
                                      "title":"unittest patch",
                                      "release_date":"04-05-2010"
                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_modify_actor_out_of_range(self):
        res = self.client().patch('/actors/100',
                                  headers={'Authorization':'Bearer ' +self.executive_producer},
                                  json={
                                      "name":"Ahmed",
                                      "birth_date":"02-10-1980",
                                      "gender":"male"
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
                                  headers={'Authorization':'Bearer ' +self.executive_producer},
                                  json={
                                      "name":"Ahmed",
                                      "birth_date":"02-10-1980",
                                      "gender":"male"
                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie_out_of_range(self):
        res = self.client().delete('/movies/100',
                                   headers={'Authorization':'Bearer ' +self.executive_producer}
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
                                   headers={'Authorization':'Bearer ' +self.executive_producer}
                                   )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor_out_of_range(self):
        res = self.client().delete('/actors/100',
                                   headers={'Authorization':'Bearer ' +self.executive_producer}
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
                                   headers={'Authorization':'Bearer ' +self.executive_producer}
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
                                headers={'Authorization':'Bearer ' +self.casting_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_movies_director(self):
        res = self.client().get('/movies',
                                headers={'Authorization':'Bearer ' +self.casting_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_actors_assistant(self):
        res = self.client().get('/actors',
                                headers={'Authorization':'Bearer ' +self.casting_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_actors_director(self):
        res = self.client().get('/actors',
                                headers={'Authorization':'Bearer ' +self.casting_director})
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
                                  headers={'Authorization':'Bearer ' +self.casting_assistant},
                                  json={
                                      "title":"unittest patch",
                                      "release_date":"04-05-2010"
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
                                  headers={'Authorization':'Bearer ' +self.casting_director},
                                  json={
                                      "title":"patched by director",
                                      "release_date":"04-05-2010"
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
                                  headers={'Authorization':'Bearer ' +self.casting_assistant},
                                  json={
                                      "name":"Ahmed",
                                      "birth_date":"02-10-1980",
                                      "gender":"male"
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
                                  headers={'Authorization':'Bearer ' +self.casting_director},
                                  json={
                                      "name":"Ahmed",
                                      "birth_date":"02-10-1980",
                                      "gender":"male"
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
                                   headers={'Authorization':'Bearer ' +self.casting_assistant}
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
                                   headers={'Authorization':'Bearer ' +self.casting_director}
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
                                   headers={'Authorization':'Bearer ' +self.casting_assistant}
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
                                   headers={'Authorization':'Bearer ' +self.casting_director}
                                  )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
