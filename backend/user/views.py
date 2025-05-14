from rest_framework import viewsets
from .models import Passenger
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from .forms import RegisterForm
from django.contrib import messages

# class PassengerViewSet(viewsets.ModelViewSet):
#     queryset = Passenger.objects.all()
#     serializer_class = PassengerSerializer


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('base')
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})

# Выход из аккаунта
@login_required
@require_http_methods(["GET", "POST"])
def custom_logout(request):
    logout(request)
    return redirect('base')

def home_view(request):
    return render(request, 'base.html')

def login_view(request):
    if request.method == 'POST':
        form = Passenger(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('base')
            else:
                messages.error(request, 'Неверный email или пароль.')
    else:
        form = Passenger()
    return render(request, 'login.html', {'form': form})