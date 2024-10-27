from django.views.generic import TemplateView, DetailView
from django.views import View
from datetime import datetime
from .api_services import TMDBClient
from django.shortcuts import render, redirect
from django.http import JsonResponse

class TrendingMovies(TemplateView):
    template_name = 'movies/home.html'
    
    def get(self, request):
        movies = []
        queryData = TMDBClient.fetch_week_trending_movies()
        genre_map = TMDBClient.fetch_genre_ids()

        movies = setup_response_data(queryData, genre_map, 'w500')
        context = {
            'trendingMovies': movies
        }

        return self.render_to_response(context)


class ItemsSearch(TemplateView):
    template_name = 'movies/search.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        if query:
            queryData = TMDBClient.search_items(query)
        else:
            return redirect('home')
        genre_map = TMDBClient.fetch_genre_ids()

        items = setup_response_data(queryData, genre_map, 'w500')
        sortedItems = sorted(items, key=lambda x: x['popularity'], reverse=True)

        context = {
            'items': sortedItems,
            'query': query
        }

        return self.render_to_response(context)
    
class SearchBar(View):
    def get(self, request):
        query = request.GET.get('query', '')
        if query:
            queryData = TMDBClient.search_items(query)
        else:
            print('error not found server!')
        genre_map = TMDBClient.fetch_genre_ids()

        items = setup_response_data(queryData, genre_map, 'w200')
        sortedItems = sorted(items, key=lambda x: x['popularity'], reverse=True)

        context = {
            'searchBarItems': sortedItems,
        }

        return JsonResponse(context, safe=False)

class MovieDetailsPage(TemplateView):
    template_name = 'movies/item-details.html'
    
    def get_context_data(self, **kwargs):
        item_id = self.kwargs.get('item_id')
        media_type = self.kwargs.get('media_type')

        itemResults = setup_item_details(item_id, media_type)

        context = {
            'itemDetails': itemResults
        }
        
        return context
    
class SeriesDetailsPage(TemplateView):
    template_name = 'movies/item-details.html'
    
    def get_context_data(self, **kwargs):
        item_id = self.kwargs.get('item_id')
        media_type = self.kwargs.get('media_type')

        itemResults = setup_item_details(item_id, media_type)

        context = {
            'itemDetails': itemResults
        }
        
        return context


def setup_response_data(queryData : list, genre_map : dict, poster_quality : str) -> list:
    items = []
    for item in queryData:
            poster_url = f"https://image.tmdb.org/t/p/{poster_quality}{item.get('poster_path')}"
            genre_names = [genre_map.get(genre_id, 'Unknown') for genre_id in item.get('genre_ids', [])]
            
            items.append({
                'item_id': item.get('id'),
                'title': item.get('title') or item.get('name'),
                'release_date': item.get('release_date') or item.get('first_air_date'),
                'media_type': item.get('media_type'),
                'vote_average': item.get('vote_average'),
                'poster_url': poster_url,
                'genres': genre_names,
                'popularity': item['popularity']
            })

    for item in items:
        if item['release_date']:
            release_date = datetime.strptime(item['release_date'], "%Y-%m-%d")
            item['release_date'] = release_date.strftime("%d %B %Y")
    
    return items

def setup_item_details(item_id, media_type):
    movieDetails = []
    tvshowDetails = []
    
    if media_type == 'movie':
        queryData = TMDBClient.search_movie_details(item_id)

        poster_url = f"https://image.tmdb.org/t/p/w500{queryData['poster_path']}"
        backdrop_url = f"https://image.tmdb.org/t/p/w1280{queryData['backdrop_path']}"

        movieDetails = {
            'title': queryData['title'],
            'release_date': queryData.get('release_date'),
            'vote_average': queryData.get('vote_average'),
            'genre': queryData['genres'],
            'overview': queryData['overview'],
            'poster_url': poster_url,
            'backdrop_img': backdrop_url,
            'runtimeHours': queryData['runtime'],
            'runtimeMinutes': queryData['runtime'],
            'media_type': media_type
        }

        movieHours = queryData['runtime']//60
        movieMinutes = queryData['runtime']%60

        movieDetails['runtimeHours'] = movieHours
        movieDetails['runtimeMinutes'] = movieMinutes

        release_date = datetime.strptime(movieDetails['release_date'], "%Y-%m-%d")
        movieDetails['release_date'] = release_date.strftime("%d %B %Y")
        
        return movieDetails
    
    else:
        queryData = TMDBClient.search_series_details(item_id)

        poster_url = f"https://image.tmdb.org/t/p/w500{queryData['poster_path']}"
        backdrop_url = f"https://image.tmdb.org/t/p/w1280{queryData['backdrop_path']}"

        tvshowDetails = {
            'title': queryData['name'],
            'release_date': queryData['first_air_date'],
            'vote_average': queryData['vote_average'],
            'genre': queryData['genres'],
            'overview': queryData['overview'],
            'poster_url': poster_url,
            'backdrop_img': backdrop_url,
            'number_of_seasons': queryData['number_of_seasons'],
            'number_of_episodes': queryData['number_of_episodes'],
            'media_type': media_type
        }

        release_date = datetime.strptime(tvshowDetails['release_date'], "%Y-%m-%d")
        tvshowDetails['release_date'] = release_date.strftime("%d %B %Y")

        return tvshowDetails
        