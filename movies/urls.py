from django.urls import path
from .views import TrendingMovies, ItemPage, MoviesSearch, MoviesSearchBar

urlpatterns = [
    path('', TrendingMovies.as_view(), name='home'),
    path('movie/<int:movie_id>', ItemPage.as_view(), name='movie'),
    path('movies-search/', MoviesSearch.as_view(), name='movies-search'),
    path('movies-search-bar/', MoviesSearchBar.as_view(), name='movies-search-bar')

]
