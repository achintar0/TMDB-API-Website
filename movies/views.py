from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .api_services import TMDBClient
from .data_setup import DataSetup
from django.shortcuts import render, redirect
from django.http import JsonResponse
from accounts.models import Watchlist

class TrendingMovies(TemplateView):
    template_name = 'movies/home.html'
    
    def get(self, request):
        movies = []
        queryData = TMDBClient.fetch_week_trending_movies()
        genre_map = TMDBClient.fetch_genre_ids()

        movies = DataSetup.setup_response_data(queryData, genre_map, 'w500')
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

        items = DataSetup.setup_response_data(queryData, genre_map, 'w500')
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

        items = DataSetup.setup_response_data(queryData, genre_map, 'w200')
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

        itemResults = DataSetup.setup_item_details(item_id, media_type)

        context = {
            'itemDetails': itemResults
        }
        
        return context
    
class SeriesDetailsPage(TemplateView):
    template_name = 'movies/item-details.html'
    
    def get_context_data(self, **kwargs):
        item_id = self.kwargs.get('item_id')
        media_type = self.kwargs.get('media_type')

        itemResults = DataSetup.setup_item_details(item_id, media_type)

        context = {
            'itemDetails': itemResults
        }
        
        return context
    

class Watchlist(LoginRequiredMixin, TemplateView):
    model = Watchlist
    template_name = 'movies/watchlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        watchlistModel = self.model.objects.filter(username=self.request.user).order_by('addedOn')
        genre_map = TMDBClient.fetch_genre_ids()

        queryData = []
        
        for item in watchlistModel:
            if item.itemType == 'tv':
                queryData.append(TMDBClient.search_series_details(item.itemID))
            else:
                queryData.append(TMDBClient.search_movie_details(item.itemID))
            
        watchlistData = DataSetup.setup_response_data(queryData, genre_map, 'w500')
        
        context = {
            'watchlistData':watchlistData,
        }

        

        return context
        
        


    
    



        