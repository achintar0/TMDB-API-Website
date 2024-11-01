from django.urls import path
from .views import MoviesLogin, MoviesLogout, SignUpView, AddToWatchlist, RemoveFromWatchlist

urlpatterns = [
    path('login/', MoviesLogin.as_view(), name='login'),
    path('logout/', MoviesLogout.as_view(), name='logout'),
    path('register/', SignUpView.as_view(), name='register'),
    path('add-to-watchlist/', AddToWatchlist.as_view(), name='add-to-watchlist'),
    path('remove-from-watchlist/', RemoveFromWatchlist.as_view(), name='remove-from-watchlist'),
]
