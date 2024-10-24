from django.views.generic import TemplateView, DetailView
from django.views import View
from datetime import datetime
from .api_services import TMDBClient
from django.shortcuts import render, redirect
import random
from django.http import JsonResponse

class TrendingMovies(TemplateView):
    template_name = 'movies/home.html'
    
    def get(self, request):
        movies = []
        queryData = TMDBClient.fetch_week_trending_movies()
        genre_map = TMDBClient.fetch_genre_ids()

        movies = setup_response_data(queryData, genre_map)
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
            'title': queryData['title'] or queryData['name'],
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

        context = {
            'movie': movieDetails
        }
        
        return context


class MoviesSearch(TemplateView):
    template_name = 'movies/movies-search.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        if query:
            queryData = TMDBClient.search_movies(query)
            print(queryData)
        else:
            return redirect('home')
        genre_map = TMDBClient.fetch_genre_ids()

        movies = setup_response_data(queryData, genre_map)
        sortedMovies = sorted(movies, key=lambda x: x['popularity'], reverse=True)

        context = {
            'movies': sortedMovies,
            'query': query
        }

        return self.render_to_response(context)
    
class MoviesSearchBar(View):
    def get(self, request):
        query = request.GET.get('query', '')
        if query:
            queryData = TMDBClient.search_movies(query)
        else:
            print('error not found server!')
        genre_map = TMDBClient.fetch_genre_ids()

        movies = setup_response_data(queryData, genre_map)
        sortedMovies = sorted(movies, key=lambda x: x['popularity'], reverse=True)

        context = {
            'searchMovies': sortedMovies,
        }

        return JsonResponse(context, safe=False)


def setup_response_data(queryData : list, genre_map : dict) -> list:
    movies = []
    for movie in queryData:
            poster_url = f"https://image.tmdb.org/t/p/w200{movie.get('poster_path')}"
            genre_names = [genre_map.get(genre_id, 'Unknown') for genre_id in movie.get('genre_ids', [])]
            
            movies.append({
                'movie_id': movie['id'],
                'title': movie.get('title') or movie.get('name'),
                'formatted_release_date': movie.get('release_date') or movie.get('first_air_date'),
                'media_type': movie.get('media_type'),
                'vote_average': movie.get('vote_average'),
                'poster_url': poster_url,
                'genres': genre_names,
                'popularity': movie['popularity']
            })

    for movie in movies:
        if movie['formatted_release_date']:
            release_date = datetime.strptime(movie['formatted_release_date'], "%Y-%m-%d")
            movie['formatted_release_date'] = release_date.strftime("%d %B %Y")
    
    return movies