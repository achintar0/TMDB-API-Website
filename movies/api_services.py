from django.conf import settings
import requests

class TMDBClient:
    BASE_URL = 'https://api.themoviedb.org/3'
    
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
    
    def search_item_details(item_id, media_type):
        itemDetails = []
        url = f'{TMDBClient.BASE_URL}/{media_type}/{item_id}'

        params = {
            'api_key': settings.TMDB_API_KEY,
            'language': 'en-US'
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        return itemDetails
    
    def search_item_videos(item_id, media_type):
        itemVideos = []
        url = f'{TMDBClient.BASE_URL}/{media_type}/{item_id}/videos'

        params = {
            'api_key': settings.TMDB_API_KEY,
            'language': 'en-US'
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json().get('results', [])
            return data
        return itemVideos

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