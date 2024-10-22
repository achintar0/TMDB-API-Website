from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views import generic, View
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import CustomRegisterForm
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


    

    

