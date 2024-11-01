from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CustomRegisterForm
from .models import Watchlist
from django.http import JsonResponse
import requests


class MoviesLogin(LoginView):
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
class MoviesLogout(View):
    template_name = 'movies/home.html'

    def get(self, request):
        logout(request)
        return redirect('home')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    

class SignUpView(CreateView):
    template_name = "accounts/register.html" 
    form_class = CustomRegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        messages.success(self.request, f"{username}")

        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)

        return redirect(self.success_url)
    

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
class AddToWatchlist(View):
    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        itemTitle = request.POST.get('title')
        itemPoster = request.POST.get('poster_url')
        itemRating = request.POST.get('vote_average')
        itemType = request.POST.get('media_type')
        user = request.user

        if not Watchlist.objects.filter(username=user, itemID=item_id).exists():
            Watchlist.objects.create(
                username=user,
                itemID=item_id,
                itemTitle=itemTitle,
                itemPoster=itemPoster,
                itemRating=itemRating,
                itemType=itemType,
            )
            return JsonResponse({'success': True, "message": "Added to Watchlist!"})
        else:
            return JsonResponse({'success': False, "message": "Item already in watchlist!"})
    
        return JsonResponse({'success': False, "message": "Invalid Request!"})


class RemoveFromWatchlist(View):
    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        itemTitle = request.POST.get('title')
        itemPoster = request.POST.get('poster_url')
        itemRating = request.POST.get('vote_average')
        itemType = request.POST.get('media_type')
        user = request.user

        if not Watchlist.objects.filter(username=user, itemID=item_id).exists():
            Watchlist.objects.create(
                username=user,
                itemID=item_id,
                itemTitle=itemTitle,
                itemPoster=itemPoster,
                itemRating=itemRating,
                itemType=itemType,
            )
            return JsonResponse({'success': True, "message": "Added to Watchlist!"})
        else:
            return JsonResponse({'success': False, "message": "Item already in watchlist!"})
    
        return JsonResponse({'success': False, "message": "Invalid Request!"})

    

