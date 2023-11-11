import os
import json

from flask import Flask, request, abort, jsonify
from models import setup_db, Movie, Actor, Movie_Actor, db
from flask_cors import CORS

from auth import AuthError, requires_auth

MOVIES_PER_PAGE = 10


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        return "Udacity's FSND Captone Project" 
        
    # Route: /movies
    # MEthod: GET
    # Returns json response: success criteria, list of movies, and integer of total movies
    
    @app.route('/movies', methods=['GET'])
    def get_movies():
        # Query all movies, order by movie_id
        movies = Movie.query.order_by(Movie.id).all()

        if len(movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': movies,
            'total_movies': len(Movie.query.all())
        }), 200

    # Route: /actors
    # Method: GET list of actors
    # Returns json response: success: true, list of actors, and integer of total actors
    
    @app.route('/actors', methods=['GET'])
    def get_actors():
        actors = Actor.query.all()

        if not actors:
            abort(404)

        return jsonify({
            'success': True,
            'actors': actors,
            'total_actors': len(actors)
        }), 200

    # Route: /movies
    # Method: POST to add a new movie to the database
    # Returns json response: success: True, movie added
    # Auth: requires role to have permission to create
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(token):
        data = request.get_json()

        #try block to make sure the data received can create new movie
        try:
            new_movie = Movie(title=data['title'], release=data['release'])
            new_movie.insert()

            return jsonify({
                'success': True,
                'movie': new_movie.format()
            }), 200

        except Exception:
            ds.session.rollback()
            abort(422)

    # Route: /actors
    # Method: POST to add a new actor to the database
    # Returns json response: success: True, actor added
    # Auth: requires role to have permission to create
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(token):
        data = request.get_json()

        try:
            actor = Actor(
                name=data['name'],
                age=data['age'],
                gender=data['gender']
            )
            actor.insert()

            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200

        except Exception:
            db.session.rollback()
            abort(422)

    # Route: /movies<int:movie_id>
    # Method: PATCH to update a movie
    # Returns json response: success: True, movie updated
    # Auth: requires role to have permission to patch
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(token, movie_id):
        body = request.get_json()

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        try:
            if body.get("title"):
                movie.title = body.get('title')
            if body.get("release_date"):
                movie.release_date = body.get('release_date')

            movie.update()

            return jsonify({
                'success': True,
                'movie': [movie.format()]
            })

        except Exception:
            db.session.rollback()
            abort(400)

    # Route: /actors<int:actor_id>
    # Method: PATCH to update an actor
    # Returns json response: success: True, actor updated
    # Auth: requires role to have permission to patch
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(token, actor_id):
        body = request.get_json()

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        try:
            if body.get("name"):
                actor.name = body.get('name')
            if body.get("age"):
                actor.age = body.get('age')
            if body.get("gender"):
                actor.gender = body.get('gender')

            actor.update()

            return jsonify({
                'success': True,
                'actors': [actor.format()]
            })

        except Exception:
            db.session.rollback()
            abort(400)

    # Route: /movies<int:movie_id>
    # Method: DELETE to remove a movie from the database
    # Returns json response: success: True, movie updated
    # Auth: requires role to have permission to delete
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(token, movie_id):

        movie = Movie.query.get(movie_id)

        if movie is None:
            abort(404)

        try:
            movie.delete()
            selection = Movie.query.all()

            return jsonify({
                'success': True,
                'deleted': movie_id,
                'movies': selection,
                'total_movies': len(selection)
            })

        except Exception:
            db.session.rollback()
            abort(422)

    # Route: /actors<int:actor_id>
    # Method: DELETE to remove an actor from the database
    # Returns json response: success: True, movie updated
    # Auth: requires role to have permission to delete
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(token, actor_id):

        actor = Actor.query.get(actor_id)

        if actor is None:
            abort(404)

        try:
            actor.delete()
            selection = Actor.query.all()

            return jsonify({
                'success': True,
                'deleted': actor_id,
                'actors': selection,
                'total_actors': len(selection)
            })

        except Exception:
            db.session.rollback()
            abort(422)

    # Error Handlers

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request - invalid"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Authentication error"
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource is not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Not allowed to perform action"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Request cannot be processed"
        }), 422

    @app.errorhandler(AuthError)
    def not_auth(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error.get('description')
        }), error.status_code


    return app

app = create_app()

if __name__ == '__main__':
    app.run()
