# Capstone


### Introduction

Capstone is a Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.


### Tech Stack

Our tech stack will include:

* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations

## Running the server

From within the `./` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
python app.py;
```

To run the server, execute:

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependences
  ├── models.py *** Database models, CSRF generation, etc
  ├── auth.py *** For JWT authentication
  ├── errorhandler.py *** For handling flask abort errors
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── manage.py *** For migration the database
  ├── Procfile *** heroku commands
  ├── setup.sh *** has all needed variables for auth0 and tokens for all roles
  └── test_app.py *** a unittest file that conatins 28 tests
  ```

## Project Details

### Authorization:
All Endpoints that shown down needs JWT tokens {Authorization: Bearer `Token`} to respond, otherwise json error will return, except '/' which
return 'healthy' for test issues.

#### Roles:
    - Casting Assistant
        - Can view actors and movies
    - Casting Director
        - All permissions a Casting Assistant has and…
        - Add or delete an actor from the database
        - Modify actors or movies
    - Executive Producer
        - All permissions a Casting Director has and…
        - Add or delete a movie from the database

#### Permissions:
    - `delete:actor`
    - `get:actors`
    - `get:movies`
    - `patch:actor`
    - `patch:movie`
    - `post:actor`


### Endpoints:
The following Endpoints:
        - GET / for test, return 'healthy'
        - GET /actors and /movies
        - DELETE /actors/<int:id> and /movies/<int:id>
        - POST /create-actor and /create-movie and
        - PATCH /actors/<int:id> and /movies/<int:id>


#### GET '/actors':
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: A json object with a single keys, actors, that contains key:value pairs, each boject inside actors has the keys: id, name, birth_date, and gender, example:
{
    "actors": [
        {
            "birth_date": "Fri, 19 Dec 1986 00:00:00 GMT",
            "gender": "male",
            "id": 1,
            "name": "Ali"
        }
    ]
}

#### GET '/movies':
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: A json object a single keys, movies, that contains key:value pairs, each boject inside movies has the keys: id, title, and release_date, example:
{
    "movies": [
        {
            "id": 1,
            "release_date": "Sat, 04 May 2002 00:00:00 GMT",
            "title": "the x files"
        }
    ]
}

#### POST '/create-actor':
- Sends post requests that has a json body to add new actors.
- Request Arguments: json body with keys, name, gender, and birth_date. for example:
{"name":"Ahmed",
"gender": "male",
"birth_date": "19-12-1986"
}
- Returns all actors, success:
{
    "actors": [
        {
            "birth_date": "Fri, 19 Dec 1986 00:00:00 GMT",
            "gender": "male",
            "id": 1,
            "name": "Ahmed"
        }
    ],
    "success": true
}

#### POST '/create-movie':
- Sends post requests that has a json body to add new movies.
- Request Arguments: json body with keys, title, and release_date. for example:
{"title":"God Father",
"birth_date": "19-12-1986"
}
- Returns all movies, success:
{
    "movies": [
        {
            "release_date": "Fri, 19 Dec 1986 00:00:00 GMT",
            "id": 1,
            "title": "God Father"
        }
    ],
    "success": true
}

#### Delete '/actors/<int:id>':
- Sends request for deleteing an actor with id = actor_id.
- Returns added success, and the id of the deleted actor:
{"success": True,
"id": 19
}

#### Delete '/movies/<int:id>':
- Sends request for deleteing a movie with id = movies_id.
- Returns added success, and the id of the deleted movie:
{"success": True,
"id": 19
}

#### PACTCH '/actors/<int:id>':
- Sends request for modifying an actor with id = actor_id.
- Returns success, and all actors.

#### PATCH '/movies/<int:id>':
- Sends request for modifying a movie with id = movies_id.
- Returns success, and all movies.

#### Errors:
Error Handling Errors are returned as JSON objects in the following format:

{ "success": False, "error": 400, "message": "bad request" }


## To Run The Server

### Locally

1. Run the command :`pip install -r requirements.txt` to intall all dependencies. 

2. Excecute the file setup.sh which has the needed variables.

3. Run `python app.py` to run the server.

4. For test Run the command `python -m unittest test_app.py`



#### Implement The Server (heroku)
Run the following commands.
1. `heroku create name_of_your_app`
2. `git remote add heroku heroku_git_url`
3. `heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application`
4. `heroku config --app name_of_your_application`
5. `heroku run python manage.py db upgrade --app name_of_your_application`

### Important Information About the Project:

1. Application URL: `https://meshal-capstone-app.herokuapp.com/`
2. Heroku Repository: `https://git.heroku.com/meshal-capstone-app.git`
3. The Project Github rep: `https://github.com/mesh3l-966/FSND/tree/master/projects/capstone/`
4. Tokens are saved as variables in setup.sh
