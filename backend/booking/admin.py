from django.contrib import admin
from .models import Flight, Booking, Seat

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'departure_city', 'arrival_city', 'departure_time', 'price')
    list_filter = ('departure_city', 'arrival_city')
    search_fields = ('flight_number',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'flight', 'num_seats', 'created_at')
    list_filter = ('created_at', 'flight')
    search_fields = ('email', 'first_name', 'last_name')

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'booking')
    search_fields = ('seat_number',)
