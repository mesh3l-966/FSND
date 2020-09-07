import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

from models import setup_db, Actor, Movie, db
from auth import AuthError, requires_auth
from errorhandler import *


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization'
            )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS'
            )
        return response

    @app.route('/')
    def healthy():
        return "healthy"

    @app.route('/movies')
    @requires_auth('get:movies')
    def movies(payload):
        unformatted_movies = Movie.query.all()
        movies = [movie.format() for movie in unformatted_movies]
        result = {
            "movies": movies
            }
        return jsonify(result)

    @app.route('/actors')
    @requires_auth('get:actors')
    def actors(pyaload):
        unformatted_actors = Actor.query.all()
        actors = [actor.format() for actor in unformatted_actors]
        result = {
            "actors": actors
            }
        return jsonify(result)

    @app.route('/create-movie', methods=['POST'])
    @requires_auth('post:movie')
    def create_movie(payload):
        try:
            body = request.get_json()
            title = body['title']
            release_date = body['release_date']
            release_date = datetime.strptime(release_date, '%d-%m-%Y')
        except Exception:
            abort(400)
        try:
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
        except Exception:
            abort(500)

        unformatted_movies = Movie.query.all()
        movies = [movie.format() for movie in unformatted_movies]
        result = {
            "success": True,
            "movies": movies
            }
        return jsonify(result)

    @app.route('/create-actor', methods=['POST'])
    @requires_auth('post:actor')
    def create_actor(payload):
        try:
            body = request.get_json()
            name = body['name']
            gender = body['gender']
            birth_date = body['birth_date']
            birth_date = datetime.strptime(birth_date, '%d-%m-%Y')
        except Exception:
            abort(400)
        try:
            actor = Actor(name=name, gender=gender, birth_date=birth_date)
            actor.insert()
        except Exception:
            abort(500)

        unformatted_actors = Actor.query.all()
        actors = [actor.format() for actor in unformatted_actors]
        result = {
            "success": True,
            "actors": actors
            }
        return jsonify(result)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def modify_movie(payload, id):
        movie = Movie.query.get(id)
        if movie is None:
            abort(404)
        body = request.get_json()
        if 'title' in body:
            title = body['title']
            try:
                movie.title = title
            except Exception:
                abort(500)

        if 'release_date' in body:
            release_date = body['release_date']
            try:
                movie.release_date = datetime.strptime(release_date,
                                                       '%d-%m-%Y')
            except Exception:
                abort(500)

        try:
            movie.update()
        except Exception:
            abort(500)

        unformatted_movies = Movie.query.all()
        movies = [movie.format() for movie in unformatted_movies]
        result = {
            "success": True,
            "movies": movies
            }
        return jsonify(result)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def modify_actor(payload, id):
        actor = Actor.query.get(id)
        if actor is None:
            abort(404)
        body = request.get_json()
        if 'name' in body:
            name = body['name']
            try:
                actor.name = name
            except Exception:
                abort(500)
        if 'gender' in body:
            gender = body['gender']
            try:
                actor.gender = gender
            except Exception:
                abort(500)

        if 'birth_date' in body:
            birth_date = body['birth_date']
            try:
                actor.birth_date = datetime.strptime(birth_date, '%d-%m-%Y')
            except Exception:
                abort(500)

        try:
            actor.update()
        except Exception:
            abort(500)

        unformatted_actors = Actor.query.all()
        actors = [actor.format() for actor in unformatted_actors]
        result = {
            "success": True,
            "actors": actors
            }
        return jsonify(result)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, id):
        movie = Movie.query.get(id)
        if movie is None:
            abort(404)
        try:
            movie.delete()
        except Exception:
            abort(500)
        result = {
            "success": True,
            "delete": id
            }
        return jsonify(result)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, id):
        actor = Actor.query.get(id)
        if actor is None:
            abort(404)
        try:
            actor.delete()
        except Exception:
            abort(500)
        result = {
            "success": True,
            "delete": id
            }
        return jsonify(result)

    return app


app = create_app()
setup_db(app)
errors(app)
CORS(app, resources={r"*": {'origins': "*"}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
