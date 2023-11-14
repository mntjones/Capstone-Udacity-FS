# Capstone Project - Movies and Actor Database

The Movie Theater API supports allowing:
- 'moviegoers' to query (GET) the database for movies and actors. 
- 'managers' to read movies and actors (GET), update movies and actors (PATCH), create new items (CREATE) and delete items from the database.


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

https://dev-upxe8nh1f3uhvzh5.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=ioqoXvUFjAntA24ZIhluY2VljiKwcYc5&redirect_uri=https://127.0.0.1:8080/login-results

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




