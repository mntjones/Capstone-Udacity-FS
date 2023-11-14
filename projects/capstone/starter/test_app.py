# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import json
import os
import unittest

from app import create_app
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor

# Auth headers to test auth requirements

moviegoer_auth_header = {
    "Authorization": "Bearer {}".format(os.environ.get('MOVIEGOER_TOKEN'))
}

manager_auth_header = {
    "Authorization": "Bearer {}".format(os.environ.get('MANAGER_TOKEN'))
}

# CapstoneTest Case - defines the variables and initializes the app

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone-web-service"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # GET tests - movies and actors

    def test_get_actors(self):
        # Insert dummy actor into database.
        actor = Actor(name="Test Actor", age=30, gender="female")
        actor.insert()

        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_404_get_actors(self):
        res = self.client().get(id=100000)
        self.assertEqual(res.status_code, 405)

    def test_get_movies(self):
        # Insert dummy actor into database.
        movie = Movie(title="Test Movie", release="January 1, 2000")
        movie.insert()

        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']))

    def test_404_get_movies(self):
        res = self.client().get(id=10000)
        self.assertEqual(res.status_code, 404)

    # POST tests - movies and Actors

    def test_create_actor(self):
        new_actor_data = {
            'name': "New Actor",
            'age': 90,
            'gender': "New Male"
        } 

        res = self.client().post('/actors', data=json.dumps(new_actor_data), headers=manager_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        actor = Actor.query.get(data['actor']['id'])
        self.assertTrue(actor)

    def test_create_movie(self):
        new_movie_data = {
            'title': "New movie Title",
            'release': "New movie Release Date",
        }

        res = self.client().post('/movies', data=json.dumps(new_movie_data), headers=manager_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        movie = Movie.query.get(data['movie']['id'])
        self.assertTrue(movie)

    def test_update_actor(self):
        actor = Actor(name="Me", age="42", gender="female")
        actor.insert()

        # update the age
        actor_update = {
            'age': '37'
        } 

        res = self.client().patch(
            f'/actors/%s' % (actor.id),
            data=json.dumps(actor_update),
            headers=manager_auth_header
        )
        # load the new data with the patched age
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['age'], actor_update['age'])

    def test_not_auth_update_actor(self):
        actor_update = {
            'age': '1'
        } 

        res = self.client().patch(
            f'/actors/%s' % (actor.id),
            data=json.dumps(actor_update),
            headers=moviegoer_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['error'], 401)
        self.assertFalse(data['success'])

    def test_delete_actor(self):
        actor = Actor(name="Actor", age="25", gender="male")
        actor.insert()

        res = self.client().delete(f'/actors/%s' % actor.id, headers=manager_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_id'], actor.id)

    def test_not_auth_delete_actor(self):
        res = self.client().delete(f'/actors/%s' % actor.id, headers=moviegoer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['error'], 401)
        self.assertFalse(data['success'])

    def test_update_movie(self):
        movie = Movie(title="Movie", release="October 31, 1999")
        movie.insert()

        movie_update = {
            'release': 'December 25, 2000'
        } 

        res = self.client().patch(
            f'/movies/%s' % (movie.id),
            data=json.dumps(movie_data_patch),
            headers=manager_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], movie.title)
        self.assertEqual(data['movie']['release'], movie_update['release'])

    def test_not_auth_update_movie(self):
        movie_update = {
            'title': 'Update Movie'
        } 

        res = self.client().patch(
            f'/movies/%s' % (movie.id),
            data=json.dumps(movie_data_patch),
            headers=moviegoer_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['error'], 401)
        self.assertFalse(data['success'])

    def test_delete_movie(self):
        movie = Movie(title="Delete Movie", release="January 1, 2023")
        movie.insert()

        res = self.client().delete(f'/movies/%s' % movie.id, headers=manager_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie_id'], movie.id)

    def test_not_auth_delete_movie(self):
        res = self.client().delete(f'/movies/%s' % movie.id, headers=moviegoer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['error'], 401)
        self.assertFalse(data['success'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()