from django.urls import path
from .views import hotel_search

urlpatterns = [
    path('', hotel_search, name='hotel_search'),
]
