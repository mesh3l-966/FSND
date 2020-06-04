API Reference
Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://localhost:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

Error Handling
Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}

The API will return three error types when requests fail:

400: Bad Request
404: Resource Not Found
405: Method not allowed
422: Unprocessable Entity
500: server error, ensure your applied feilds are properly filled


Endpoints
GET '/categories'
GET '/questions'
GET '/categories/<category_id>/questions'
POST '/questions'
DELETE '/questions/<question_id>'
POST '/quizzes'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}


GET '/questions'
- Fetches a dictionary has the following key:value pairs:
- a categories-dictionary which is same as what we get from GET '/categories'
- 'currentCategory' key which in this case return Null value, 'currentCategory':null
- 'questions' key which has a value of list of questions, each question is a dictionary object. example:
'questions':[
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    }
]
-'success':True key:value pair.
-'total_questions' key which has the number of questions as a value,example: 'total_questions':15


GET '/categories/<category_id>/questions'
- Fetches all key:value pairs that are fetched by GET '/questions', but only quesitons that are related to a specific category.
- category_id is the id for the required category.




POST '/questions'
- Sends post requests that has a json body to add new questions.
- Request Arguments: json body with keys, quesiton, answer, category, and difficulty. for example:
{"question":"What is the captial of Saudi Arabia?",
"answer": "Riyadh",
"category": "3",
"difficulty": "1"
}
- Returns added quesiton, success, quesiton_id:
{"success": True,
"Question":"What is the captial of Saudi Arabia?",
"Question id": 10
}



DELETE '/questions/<question_id>'
- Sends request for deleteing a question with id = quesiton_id.
- Returns added success, total of left questions:
{"success": True,
"total qustions": 31
}


POST '/quizzes'
- Fetches a dictionary of a random quesiton.
- Request Arguments: a dictionary that has two key-value pairs:
first one: "previous_questions" which contains a value that is a list of quesitons ids that has send before.
Second one: "quiz_category" which contains a dictionary value with keys id, type.
Example:
{"previous_questions": "[14,15]",
 "quiz_category" : {"type": "Science", "id": "1"}
}
- The random question must not be in the previous_questions list, and must be from the required category.
- Example of a return question:
{
  "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  }
}



