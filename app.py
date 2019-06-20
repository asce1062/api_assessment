import json


from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)


with open('mock_data.json', "r") as file:
    all_movies = json.load(file)


def response_builder(data, status_code):
    """
    Build the jsonified response to return.
    """
    response = jsonify(data)
    response.status_code = status_code
    return response


class MovieAPI(Resource):
    """
    Get all movies by ID if provided.
    Get all movies matching the search term provided.
    """

    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('q')
        args = parser.parse_args()
        query = args['q']
        if id:
            movie_id = []
            for movie in all_movies:
                for key, value in movie.items():
                    if id == movie["id"]:
                        movie_id.append(movie)
                        break

            if not movie_id:
                return response_builder({
                    'error': 'No movie with that Id was found'
                }, 404)
            else:
                return response_builder({
                    'movie': movie_id
                }, 200)
        elif query:
            search_results = []
            for movie in all_movies:
                movie_genre = movie.get('genre')
                movie_name = movie.get('name')
                if query.lower() in movie_genre.lower()\
                        or query.lower() in movie_name.lower():
                    search_results.append(movie)
            if not search_results:
                return response_builder({
                    'error': 'No movies match the genre or name provided'
                }, 400)
            else:
                return response_builder(
                    {
                        'movies': search_results
                    }, 200)
        else:
            list_movies = []
            for movies in all_movies:
                list_movies.append(movies)
            if not movies:
                return response_builder({
                    'error': 'No movies currently in the system.'
                }, 204)
            else:
                return response_builder(
                    {
                        'movies': all_movies
                    }, 200)


api.add_resource(MovieAPI, '/movies/<int:id>', '/movies')
