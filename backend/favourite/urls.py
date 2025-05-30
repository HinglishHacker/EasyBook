from django.urls import path
from . import views

app_name = 'favourite'

urlpatterns = [
    path('', views.favourite_list, name='favourite_list'),
    path('add/<int:ticket_id>/', views.add_to_favourites, name='add_to_favourites'),
    path('remove/<int:ticket_id>/', views.remove_from_favourites, name='remove_from_favourites'),
]
