from django.urls import path
from .views import *

urlpatterns = [
    path('', TrendingMovies.as_view(), name='home'),
    path('<str:media_type>/<int:item_id>', SeriesDetailsPage.as_view(), name='series-details'),
    path('<str:media_type>/<int:item_id>', MovieDetailsPage.as_view(), name='movie-details'),
    path('search/', ItemsSearch.as_view(), name='search'),
    path('items-search-bar/', SearchBar.as_view(), name='items-search-bar'),
    path("watchlist/", Watchlist.as_view(), name="watchlist"),
]
