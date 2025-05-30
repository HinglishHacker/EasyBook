from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'car_rental'

urlpatterns = [
    path('search/', views.car_search, name='search')
]
