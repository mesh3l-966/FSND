import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from errorhandler import *

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  errors(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"*":{'origins': "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods','GET, POST, PATCH, DELETE, OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    cat_dict = {}
    for cat in categories:
      cat_dict[cat.id] = cat.type
    return jsonify({'categories':cat_dict})
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def questions():
    all_ques = Question.query.all()
    questions = pagination(request, all_ques)
    if not len(questions):
      abort(404)
    categories = Category.query.all()
    formatted_ques = [ques.format() for ques in questions]
    #creating a dictionary with category id as key
    #and category type as value
    cat_dict = {}
    for cat in categories:
      cat_dict[cat.id] = cat.type
    
    result = {
      'success': True,
      'questions': formatted_ques,
      'total_questions': len(all_ques),
      'categories': cat_dict,
      'currentCategory': None
    }
    return jsonify(result)


  def pagination(request, selection):
    page = request.args.get('page',1, int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    return selection[start:end]
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:ques_id>', methods=['DELETE'])
  def delete_question(ques_id):
    question = Question.query.get(ques_id)
    if question is None:
      abort(422)
    
    question.delete()

    return jsonify({
      'success': True,
      'question id': question.id,
      'total qustions': len(Question.query.all())
       })
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    data = request.get_json()
    if 'searchTerm' in data:

      all_ques = Question.query.filter(Question.question.ilike('%'+ data['searchTerm']+'%')).all()
      if all_ques is None:
        abort(404)

      questions = pagination(request,all_ques)
      result = {
        'questions': [question.format() for question in questions],
        'totalQuestions': len(all_ques),
        'currentCategory': None,
        'success': True 
      }
      return jsonify(result)
    try:
      question = data['question']
      answer = data['answer']
      difficulty = data['difficulty']
      category = data['category']
    except:
      abort(400)

    ques = Question(question=question, answer=answer, difficulty=difficulty, category=category)
    ques.insert()

    return jsonify({
      'success': True,
      'Question added': ques.question,
      'Question id': ques.id
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:cat_id>/questions')
  def questions_by_cat(cat_id):
    all_ques = Question.query.filter_by(category=cat_id).all()
    questions = pagination(request, all_ques)
    if not len(questions):
      abort(404)
    form_ques = [ques.format() for ques in questions]
    result = {
      'success': True,
      'questions': form_ques,
      'total_questions': len(all_ques),
      'currentCategory': Category.query.get(cat_id).type
    }
    return jsonify(result)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    data = request.get_json()
    previous_questions = data['previous_questions']
    quiz_category = data['quiz_category']['id']
    if len(previous_questions) == len(Question.query.all()):
      abort(404)
    if quiz_category == 0:
      questions = Question.query.all()
    else:
      questions = Question.query.filter(Question.category==quiz_category).all()
    
    question = random.choice(questions)
    while(str(question.id) in previous_questions):
      question = random.choice(questions)

    return jsonify({
            'question': question.format(),
            'success': True
        })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  #created in errorhandler.py file
  return app

# if __name__ == "__main__":
#     create_app()

    