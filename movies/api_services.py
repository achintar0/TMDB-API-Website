from django.conf import settings
import requests

class TMDBClient:
    BASE_URL = 'https://api.themoviedb.org/3'

    def fetch_day_trending_movies():
        movies = []
        url = f'{TMDBClient.BASE_URL}/trending/movie/day'
        params = {
            'api_key': settings.TMDB_API_KEY,
            'page': 1
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('results', [])
        return movies
    
    def fetch_week_trending_movies():
        movies = []
        url = f'{TMDBClient.BASE_URL}/trending/movie/week'
        params = {
            'api_key': settings.TMDB_API_KEY,
            'page': 1
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('results', [])
        return movies
        
            
    def fetch_genre_ids():
        genre_map = []
        url = f'{TMDBClient.BASE_URL}/genre/movie/list'

        params = {
                'api_key': settings.TMDB_API_KEY,
                'language': 'en-US',
            }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            genres = response.json().get('genres', [])
            genre_map = {genre['id']: genre['name'] for genre in genres}
            return genre_map
        return genre_map
    
    def search_movie_details(movie_id):
        movieDetails = []
        url = f'{TMDBClient.BASE_URL}/movie/{movie_id}'

        params = {
            'api_key': settings.TMDB_API_KEY,
            'language': 'en-US'
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            movieDetails = response.json()
            return movieDetails
        return movieDetails
