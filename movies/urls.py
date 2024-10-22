from django.urls import path
from .views import TrendingMovies, ItemPage

urlpatterns = [
    path('', TrendingMovies.as_view(), name='home'),
    path('movie/<int:movie_id>', ItemPage.as_view(), name='movie')
]
