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
  └── test_app.py *** a unittest file that conatins 28 tests
  ```
## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `delete:actor`
    - `get:actors`
    - `get:movies`
    - `patch:actor`
    - `patch:movie`
    - `post:actor`
6. Create new roles for:
    - Casting Assistant
        - Can view actors and movies
    - Casting Director
        - All permissions a Casting Assistant has and…
        - Add or delete an actor from the database
        - Modify actors or movies
    - Executive Producer
        - All permissions a Casting Director has and…
        - Add or delete a movie from the database
7. Create the following Endpoints:
        - GET /actors and /movies
        - DELETE /actors/ and /movies/
        - POST /actors and /movies and
        - PATCH /actors/ and /movies/

8. Test your endpoints with test_app.py (unittest). 
    - One test for success behavior of each endpoint
    - One test for error behavior of each endpoint
    - At least two tests of RBAC for each role


### Implement The Server

After creating an account in heroku, enter the following commands:

1. `heroku create name_of_your_app`
2. `git remote add heroku heroku_git_url`
3. `heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application`
4. `heroku config --app name_of_your_application`


### Important Information About the Project:

1. Application URL: `https://meshal-capstone-app.herokuapp.com/`
2. Heroku Repository: `https://git.heroku.com/meshal-capstone-app.git`
3. The Project Github rep: `https://github.com/mesh3l-966/FSND/tree/master/projects/capstone/`
4. Excecutive Producer Token: `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1mbC04UmhnLXIwZVdNZWotdXZzVyJ9.eyJpc3MiOiJodHRwczovL21lc2hhbC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkZWJmYTFhMzZlYjIwMDE5N2QyOWMxIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTk0OTA4MjEsImV4cCI6MTU5OTU3NzIyMSwiYXpwIjoiZHlINmxDVGFsUnB3T2ZhWmZiUVY2MlFZeUhFVWx0TnIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.7bhuwSVSlCZUm3UtJIEe5pEqzb0p7jC6GTcmaXrCFEX_7wKODf1DU_0Wjsc83LDU7Q1imYMHKeZlxghvglwG3ISYpJJJGKdno6N1ER9qkezjQ7qQDU3FpyUNRs7LR-0xpXP-Li-V9KLVuyyKvRG57ZgkEgEjK3ES28V8kKZq_mLZqQb3jLygscSUZME5dnKRXkQoeKin_rdRtWKbdf_V7O7MRXBKAstQQDFmR9pZrl0bMXz7goYZEBlMSLXDKj_nt8ASfCoyFNwHaeMO523Sb5rCUxAs1vvEzr2pNQ8Lq0FnT8lbLU0ib6Zf9cCg51ZrpA7K5j9XS7yi0gM2VLn7bQ`
5. Casting Director Token: `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1mbC04UmhnLXIwZVdNZWotdXZzVyJ9.eyJpc3MiOiJodHRwczovL21lc2hhbC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY1NTU3ZjkzOTdiNzAwMDY3NTA5NjkwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTk0OTA5NjQsImV4cCI6MTU5OTU3NzM2NCwiYXpwIjoiZHlINmxDVGFsUnB3T2ZhWmZiUVY2MlFZeUhFVWx0TnIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.oeQxcVmz8kIj4kV3mx9Qx0LjORbSUvLxzKdzf-0VFHhxtBcSCy_Irq5aQl3m8NuzUHzXS5vcHVE9vTlsNMQHUF5naO2JGghNHYKsmVK0A63TKT1DpcTCrvHtEhRzKysddcjWM5dRZNpETLYykRulwZydq2_9_szQ24OhSNmyMkhKvbMR8op8dFguJaLD2gpp0losGXedKpf_OfHdTubIGzKrN4K3i18lxmlYxQX-M5A6Pj4p4gJb_eHVt3CdSJF8JBLj820N9vkzc2-dPuizLPi9EwShcmR-jBeqA40JNrTjZEuvL5uEoaj5dWFHUD4AuU9y-4bcEKJoBaSjs160mQ`
6. Casting Assistant Token: `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1mbC04UmhnLXIwZVdNZWotdXZzVyJ9.eyJpc3MiOiJodHRwczovL21lc2hhbC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY1NTU3ZjkzOTdiNzAwMDY3NTA5NjkwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTk0OTEwNTEsImV4cCI6MTU5OTU3NzQ1MSwiYXpwIjoiZHlINmxDVGFsUnB3T2ZhWmZiUVY2MlFZeUhFVWx0TnIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.a2FIepcmDo4fVK5szysuQmYcDWdBa0TQh3b09py8h4Oryr715ce_qjZrtnjpp1vLFYnq6M0qZGcjuoklsVGKmcOP1Z2xY-FrB-uRiq1rHXyDPXCn5xRA2c5bO8CGLE_3u0hihhmeVKyqaBufyLq4RBg63uDKgsElA0lyEbFlCJ0BoD5qtL6tFEEHZ0e148JMKq7iAHceuyPdXiapn20ciVFYITyDgtisGxmp9ow1bKJvaQcXNsd7UTFv1GmRfzUI2-cmngHSRYWI7P0EXWP-XCdsA5RN-3_Sae9Dcw_1YSdpBp8Fjfd8FPkCm0cDVybcuUhTa0aRS7LL4VqGh0o_IA`
