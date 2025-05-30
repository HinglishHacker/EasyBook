from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('search/', views.search_flights, name='flight_list'),
    path('form_amadeus/', views.amadeus_book_view, name='booking_form_amadeus'),  #booking_form_amadeus
    path('success-amadeus/', views.booking_success_amadeus, name='booking_success_amadeus'),
    path('flights/', views.search_flights, name='flights'),
    path('', views.search_flights, name='search_flights'),
    path('booking/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('history/', views.booking_history, name='booking_history'),
    path('booking/history/', views.booking_history, name='booking_history'),
    path('booking/amadeus-book/', views.amadeus_book_view, name='amadeus_book'),
    path('booking/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),

]

