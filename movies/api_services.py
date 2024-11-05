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
    
    def search_movie_details(item_id):
        movieDetails = []
        url = f'{TMDBClient.BASE_URL}/movie/{item_id}'

        params = {
            'api_key': settings.TMDB_API_KEY,
            'language': 'en-US'
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        return movieDetails
    
    def search_series_details(item_id):
        seriesDetails = []
        url = f'{TMDBClient.BASE_URL}/tv/{item_id}'

        params = {
            'api_key': settings.TMDB_API_KEY,
            'language': 'en-US'
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        return seriesDetails

    def search_series_video(item_id):
        serieVideos = []
        url = f'{TMDBClient.BASE_URL}/tv/{item_id}/videos'

        params = {
            'api_key': settings.TMDB_API_KEY,
            'language': 'en-US'
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        return serieVideos
    
    def search_movie_video(item_id):
        movieVideos = []
        url = f'{TMDBClient.BASE_URL}/movie/{item_id}/videos'

        params = {
            'api_key': settings.TMDB_API_KEY,
            'language': 'en-US'
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        return movieVideos

    @staticmethod
    def search_items(query):
        url =  f'{TMDBClient.BASE_URL}/search/multi'

        params = {
            'api_key': settings.TMDB_API_KEY,
            'query': query,
            'page': '1',
        }

        itemData = []
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json().get('results', [])
            return data
        return itemData