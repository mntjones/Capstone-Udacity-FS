# Capstone Project - Movies and Actor Database

This project models a movie theater that is responsible for showing cultural movies with title and release date and providing info about prominent actors with their name, age and gender.

The Movie Theater API supports allowing:
- 'moviegoers' to query (GET) the database for movies and actors. 
- 'managers' to read movies and actors (GET), update movies and actors (PATCH), create new items (CREATE) and delete (DELETE) items from the database.


## Getting Started

### Installing Dependencies

#### Python 3.9.0

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by navigating to the folder where this README doc resides and running:

```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the requirements.txt file.

## Running the App

API can be accessed through: https://capstone-web-service-sbnk.onrender.com

Authentication:
https://dev-upxe8nh1f3uhvzh5.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=ioqoXvUFjAntA24ZIhluY2VljiKwcYc5&redirect_uri=https://127.0.0.1:8080

to get the access token

Add header ``` Authorization : Bearer {your_access_token}```

## Auth0 Roles

Auth0 information for endpoints that require authentication can be found in setup.sh.


## Testing

cd into capstone -> starter and run:
```python -m test_app.py ```


## Error Handling

Errors are returned in JSON format

The API will return these error types when requests fail:

{
  "success": False,
  "error": 400,
  "message": "Bad Request - invalid"
}

{
  "success": False,
  "error": 401,
  "message": "Authentication error"
}

{
  "success": False,
  "error": 404,
  "message": "Resource is not found"
}

{
  "success": False,
  "error": 405,
  "message": "Not allowed to perform action"
}

{
  "success": False,
  "error": 422,
  "message": "Request cannot be processed"
}

## Endpoints

GET /movies
Returns a list of all the movies and a number of total movies.

Sample response output:
```
{
    'success': true,
    'movies': [
        {
            "id": 1,
            "title": "Annie",
            "release_date": "January 1, 1981"
            
        },
        {
            "id": 2,
						"title": "Zoolander",
            "release_date": "December 31, 2014",
        }
    ],
    'total_movies': 2
}
```

POST /movies
Creates a new movie using the title and release date.
Returns the ID of the created movie, success value, and the movie created.

Sample response output:
```
{
    'success': True,
    'movie': {
            "id": 3,
            "title": "Moana"
            "release_date": "August 14, 2016"
        		}
}
```

UPDATE /movies/{movie_id}
Updates the movie based on the given movie ID using the updated title and/or release date.
Returns the success value and the updated movie.

Sample response output:
```
{
    'success': True,
    'movie': {
            "id": 3,
            "title": "Moana",
            "release_date": "August 1, 2022"
        		}
}

```

DELETE /movies/{movie_id}
Deletes the movie based on the given movie ID.
Returns the success value, the ID of the deleted movie, the list of all the movies, and the number of total movies.

Sample response output:
```
{
    'success': True,
    'deleted': 1,
    'movies': [
        {
            "id": 2,
            "title": "Zoolander",
            "release_date": "December 31, 2014"
            
        },
        {
            "id": 3,
            "title": "Moana",
            "release_date": "August 1, 2022"
        }
    ],
    'total_movies': 2
}
```
GET /actors
Returns a list of all the actors and a number of total actors.

Sample response output:
```
{
    'success': True,
    'actors': [
	    {	
	    	"id": 1,
	    	"name": "Actor 1",
	      "age": 32,
	      "gender": "female",
	    },
	    {
	      "id": 2,
	    	"name": "Actor 2",
	      "age": 12,
	      "gender": "male",
	    },
    ]
    'total_actors': 2
}

```

POST /actors
Creates a new actor using the name, age, and gender.
Returns the ID of the created actor, success value, and the created actor details

Sample response output:
```
{
    'success': True,
    'actor': {
    		"id": 3,
	    	"name": "Actor 3",
	      "age": 55,
	      "gender": "female"
	    }
}
```

UPDATE /actors/{actor_id}
Updates the actor based on the given actor ID using the updated name, age, and/or gender.
Returns the success value and the updated actor.

Sample response output:
```
{
    'success': True,
    'actor': {
    		"id": 3,
	    	"name": "Actor 3",
	      "age": 85,
	      "gender": "female"
	    }
}
```
DELETE /actors/{actor_id}
Deletes the actor based on the given actor ID.
Returns the success value, the ID of the deleted actor, a list of actors, and the number of total actors.

Sample response output:
```
{
    'success': True,
    'deleted': 2,
    'actors': [
	    {	
	    	"id": 1,
	    	"name": "Actor 1",
	      "age": 32,
	      "gender": "female",
	    },
	    {
	      "id": 3,
	    	"name": "Actor 3",
	      "age": 85,
	      "gender": "female",
	    },
    ]
    'total_actors': 2
}
```

