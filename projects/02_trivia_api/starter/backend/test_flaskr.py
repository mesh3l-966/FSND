import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "triviatest"

        self.database_path = "postgresql://{}/{}".format('postgres:laug999@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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

    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_request_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['message'],'resource not found')

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_request_beyond_valid_category(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['message'],'resource not found')

    def test_create_new_question(self):
        res = self.client().post('/questions', json={"question":"from where?",
                                                    "answer": "from test_flaskr",
                                                        "category": "1",
                                                        "difficulty": "2"
                                                    })
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['Question added'],'from where?')
        self.assertEqual(res.status_code, 200)
    
    def test_422_delete_beyond_valid_questions(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Unprocessable Entity')

    def test_delete_question(self):
        self.ques = 'What is my name?'
        self.answer = 'Meshal'
        self.category = 3
        self.difficulty = 1
        self.question = Question(self.ques,self.answer,self.category,self.difficulty)
        self.question.id = 100
        self.question.insert()

        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
    
    def test_search_for_questions(self):
        res = self.client().post('/questions', json={'searchTerm':'whose'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()