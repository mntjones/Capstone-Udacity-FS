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
    # Returns json response: success criteria, list of movies, and integer of total movies
    
    @app.route('/movies')
    def get_movies():
        # Query all movies, order by movie_id
        selection = Movie.query.order_by(Movie.id).all()
        current_movies = paginate_data(request, selection)

        if len(current_movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': current_movies,
            'total_movies': len(Movie.query.all())
        })

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
