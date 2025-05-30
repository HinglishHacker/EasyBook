from django.db import models
from django.utils import timezone

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.flight_number}: {self.departure_city} → {self.arrival_city}"


class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, null=True, blank=True)  # для локальных рейсов
    departure_city = models.CharField(max_length=100, blank=True)  # для Amadeus
    arrival_city = models.CharField(max_length=100, blank=True)    # для Amadeus
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    extra_phone = models.CharField(max_length=20, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    citizenship = models.CharField(max_length=50, blank=True)
    passport_number = models.CharField(max_length=50, blank=True)
    passport_expiry = models.DateField(null=True, blank=True)
    passport_country = models.CharField(max_length=50, blank=True)
    num_seats = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.flight:
            return f"{self.first_name} {self.last_name} - {self.flight.flight_number}"
        return f"{self.first_name} {self.last_name} - {self.departure_city} → {self.arrival_city}"


class Seat(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)

    def __str__(self):
        return self.seat_number
