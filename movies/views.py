from django.views.generic import TemplateView, DetailView
from datetime import datetime
from .api_services import TMDBClient
from django.shortcuts import render, redirect
import random

class TrendingMovies(TemplateView):
    template_name = 'movies/home.html'
    
    def get(self, request):
        movies = []
        data = TMDBClient.fetch_week_trending_movies()
        genre_map = TMDBClient.fetch_genre_ids()

        for movie in data:
            poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
            
            
            genre_names = [genre_map.get(genre_id, 'Unknown') for genre_id in movie.get('genre_ids', [])]
            
            movies.append({
                'movie_id': movie['id'],
                'title': movie['title'],
                'formatted_release_date': movie['release_date'],
                'vote_average': movie['vote_average'],
                'poster_url': poster_url,
                'genres': genre_names,
            })


        for movie in movies:
            if movie['formatted_release_date']:
                release_date = datetime.strptime(movie['formatted_release_date'], "%Y-%m-%d")
                movie['formatted_release_date'] = release_date.strftime("%d %B %Y")

        context = {
            'movies': movies
        }

        return self.render_to_response(context)

class ItemPage(TemplateView):
    template_name = 'movies/item_page.html'
    
    def get_context_data(self, **kwargs):
        movie_id = self.kwargs.get('movie_id')
        movieDetails = []
        queryData = TMDBClient.search_movie_details(movie_id)

        poster_url = f"https://image.tmdb.org/t/p/w500{queryData['poster_path']}"
        backdrop_url = f"https://image.tmdb.org/t/p/w1280{queryData['backdrop_path']}"

        

        movieDetails = {
            'title': queryData['title'],
            'release_date': queryData['release_date'],
            'vote_average': queryData['vote_average'],
            'genre': queryData['genres'],
            'overview': queryData['overview'],
            'poster_url': poster_url,
            'backdrop_img': backdrop_url,
            'runtimeHours': queryData['runtime'],
            'runtimeMinutes': queryData['runtime']
        }

        movieHours = queryData['runtime']//60
        movieMinutes = queryData['runtime']%60

        movieDetails['runtimeHours'] = movieHours
        movieDetails['runtimeMinutes'] = movieMinutes

        release_date = datetime.strptime(movieDetails['release_date'], "%Y-%m-%d")
        movieDetails['release_date'] = release_date.strftime("%d %B %Y")

        print(movieDetails)

        context = {
            'movie': movieDetails
        }
        
        return context



