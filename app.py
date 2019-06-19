import json

from flask import Flask, jsonify
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


with open('mock_data.json', "r") as file:
    all_movies = json.load(file)


def response_builder(data, status_code=200):
    """Build the jsonified response to return."""
    response = jsonify(data)
    response.status_code = status_code
    return response


class MovieAPI(Resource):
    """
    Get all movies by ID if provided
    """

    def get(self, id=None):
        if id:
            movie_ids = []
            for movie in all_movies:
                for key, value in movie.items():
                    if id == movie["id"]:
                        movie_ids.append(movie)

            if len(movie_ids) < 1:
                return response_builder({
                    "message": "No movie with that Id was found",
                }, 404)
            else:
                return response_builder({
                    "movie": movie_ids[0]
                }, 200)
        else:
            list_movies = []
            for movie in all_movies:
                list_movies.append({
                    'id': movie["id"],
                    "name": movie["name"],
                    "showing_time": movie["showing_time"],
                    "duration": movie["duration"],
                    "genre": movie["genre"],
                    "release_date": movie["release_date"],
                })
            return response_builder(
                {
                    "movies": all_movies,
                }, 200
            )
            if not all_movies:
                return response_builder({
                    "message": "No movies in the system currently.",
                }, 400)


api.add_resource(MovieAPI, '/movies/<int:id>', '/movies', endpoint="movie")
