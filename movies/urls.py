from django.urls import path
from .views import TrendingMovies, MovieDetailsPage, SeriesDetailsPage, ItemsSearch, SearchBar

urlpatterns = [
    path('', TrendingMovies.as_view(), name='home'),
    path('<str:media_type>/<int:item_id>/', SeriesDetailsPage.as_view(), name='series-details'),
    path('<str:media_type>/<int:item_id>', MovieDetailsPage.as_view(), name='movie-details'),
    path('search/', ItemsSearch.as_view(), name='search'),
    path('items-search-bar/', SearchBar.as_view(), name='items-search-bar')

]
