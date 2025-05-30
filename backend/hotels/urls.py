from django.urls import path
from .views import hotel_search

app_name = 'hotels'

urlpatterns = [
    path('', hotel_search, name='hotel_search'),
]
