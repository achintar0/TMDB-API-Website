from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .api_services import TMDBClient
from .data_setup import DataSetup
from django.shortcuts import render, redirect
from django.http import JsonResponse
from accounts.models import Watchlist
from django.contrib.auth.mixins import LoginRequiredMixin


class TrendingMovies(LoginRequiredMixin, TemplateView):
    template_name = 'movies/home.html'
    
    def get(self, request):
        if self.request.user:
            user = self.request.user
        else:
            user = None
        movies = []
        queryData = TMDBClient.fetch_week_trending_movies()
        genre_map = TMDBClient.fetch_genre_ids()

        movies = DataSetup.setup_response_data(queryData, genre_map, 'w500', user)
        context = {
            'trendingMovies': movies
        }

        return self.render_to_response(context)


class ItemsSearch(LoginRequiredMixin, TemplateView):
    template_name = 'movies/search.html'

    def get(self, request, *args, **kwargs):
        if self.request.user:
            user = self.request.user
        else:
            user = None
        query = request.GET.get('query', '')
        if query:
            queryData = TMDBClient.search_items(query)
        else:
            return redirect('home')
        genre_map = TMDBClient.fetch_genre_ids()

        items = DataSetup.setup_response_data(queryData, genre_map, 'w500', user)
        sortedItems = sorted(items, key=lambda x: x['popularity'], reverse=True)

        context = {
            'items': sortedItems,
            'query': query
        }

        return self.render_to_response(context)
    
class SearchBar(View):
    def get(self, request):
        user = self.request.user
        query = request.GET.get('query', '')
        if query:
            queryData = TMDBClient.search_items(query)
        else:
            print('error not found server!')
        genre_map = TMDBClient.fetch_genre_ids()

        items = DataSetup.setup_response_data(queryData, genre_map, 'w200', user)
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
        user = self.request.user

        itemResults = DataSetup.setup_item_details(item_id, media_type, user)

        context = {
            'itemDetails': itemResults
        }
        
        return context
    
class SeriesDetailsPage(TemplateView):
    template_name = 'movies/item-details.html'
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        item_id = self.kwargs.get('item_id')
        media_type = self.kwargs.get('media_type')

        itemResults = DataSetup.setup_item_details(item_id, media_type, user)

        context = {
            'itemDetails': itemResults
        }
        
        return context
    

class Watchlist(LoginRequiredMixin, TemplateView):
    model = Watchlist
    template_name = 'movies/watchlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        watchlistModel = self.model.objects.filter(username=self.request.user).order_by('-addedOn')

        
        watchlistDataMovies = []
        watchlistDataSeries = []

        for item in watchlistModel:
            poster_url = f"https://image.tmdb.org/t/p/w500{item.itemPoster}"
            if item.itemType == 'tv':
                watchlistDataSeries.append({
                    'item_id': item.itemID,
                    'title': item.itemTitle,
                    'poster_url': poster_url,
                    'vote_average': item.itemRating,
                    'media_type': item.itemType,
                })
            else:
                watchlistDataMovies.append({
                    'item_id': item.itemID,
                    'title': item.itemTitle,
                    'poster_url': poster_url,
                    'vote_average': item.itemRating,
                    'media_type': item.itemType,
                })
 
        context = {
            'watchlistDataMovies':watchlistDataMovies,
            'watchlistDataSeries':watchlistDataSeries,

        }
        return context
        
        


    
    



        