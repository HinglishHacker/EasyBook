import random
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Flight, Booking, Seat
from .forms import FlightSearchForm, BookingForm
from booking.amadeus_api import search_flights as search_amadeus_flights

def generate_seat_numbers(count):
    import string
    rows = list(string.ascii_uppercase)
    return [f"{rows[i // 6]}{(i % 6) + 1}" for i in range(count)]

def search_flights(request):
    form = FlightSearchForm(request.GET or None)
    flights = []
    amadeus_flights = []
    search_performed = False

    popular_cities = [
        {"name": "Абудаби", "code": "AUH"}, {"name": "Амстердам", "code": "AMS"}, {"name": "Афины", "code": "ATH"},
        {"name": "Бангкок", "code": "BKK"}, {"name": "Барселона", "code": "BCN"}, {"name": "Баку", "code": "GYD"},
        {"name": "Берлин", "code": "BER"}, {"name": "Брюссель", "code": "BRU"}, {"name": "Вена", "code": "VIE"},
        {"name": "Варшава", "code": "WAW"}, {"name": "Гонконг", "code": "HKG"}, {"name": "Дели", "code": "DEL"},
        {"name": "Доха", "code": "DOH"}, {"name": "Дубай", "code": "DXB"}, {"name": "Казань", "code": "KZN"},
        {"name": "Киев", "code": "IEV"}, {"name": "Лиссабон", "code": "LIS"}, {"name": "Лондон", "code": "LON"},
        {"name": "Лос-Анджелес", "code": "LAX"}, {"name": "Мадрид", "code": "MAD"}, {"name": "Майами", "code": "MIA"},
        {"name": "Милан", "code": "MXP"}, {"name": "Минск", "code": "MSQ"}, {"name": "Москва", "code": "SVO"},
        {"name": "Нью-Йорк", "code": "NYC"}, {"name": "Неаполь", "code": "NAP"}, {"name": "Париж", "code": "CDG"},
        {"name": "Прага", "code": "PRG"}, {"name": "Рига", "code": "RIX"}, {"name": "Рим", "code": "FCO"},
        {"name": "Санкт-Петербург", "code": "LED"}, {"name": "Сеул", "code": "ICN"}, {"name": "Сингапур", "code": "SIN"},
        {"name": "Стамбул", "code": "IST"}, {"name": "Ташкент", "code": "TAS"}, {"name": "Токио", "code": "NRT"},
        {"name": "Торонто", "code": "YYZ"}, {"name": "Урумчи", "code": "URC"}, {"name": "Франкфурт", "code": "FRA"},
        {"name": "Хельсинки", "code": "HEL"}, {"name": "Чикаго", "code": "ORD"}, {"name": "Шанхай", "code": "PVG"},
        {"name": "Шарджа", "code": "SHJ"}, {"name": "Штутгарт", "code": "STR"},
    ]

    alternative_destinations = random.sample(popular_cities, 5)

    if form.is_valid():
        search_performed = True
        departure = form.cleaned_data['departure_city'].upper()
        arrival = form.cleaned_data['arrival_city'].upper()
        date = form.cleaned_data['departure_date']
        cabin_class = request.GET.get('cabin_class')
        adults = int(request.GET.get('adults', 1))

        if departure == arrival:
            return render(request, 'booking/flight_list.html', {
                'form': form,
                'flights': [],
                'amadeus_flights': [],
                'popular_cities': popular_cities,
                'alternative_destinations': alternative_destinations,
                'form_error': "Вы не можете вылететь и прилететь в один и тот же город.",
                'search_performed': search_performed
            })

        flights = Flight.objects.filter(
            departure_city__iexact=departure,
            arrival_city__iexact=arrival,
            departure_time__date=date
        )

        seen = set()
        amadeus_data = search_amadeus_flights(departure, arrival, date, cabin_class, adults)

        for offer in amadeus_data[:10]:
            try:
                segment = offer["itineraries"][0]["segments"][0]
                price = float(offer["price"]["total"])
                dep_code = segment["departure"]["iataCode"]
                arr_code = segment["arrival"]["iataCode"]

                if dep_code != departure or arr_code != arrival:
                    continue

                cabin = offer.get("travelerPricings", [{}])[0].get("fareDetailsBySegment", [{}])[0].get("cabin", "ECONOMY")

                key = (dep_code, arr_code, price, cabin)
                if key in seen:
                    continue
                seen.add(key)

                amadeus_flights.append({
                    "departure": dep_code,
                    "arrival": arr_code,
                    "price": price,
                    "class": cabin
                })
            except Exception as e:
                print("❌ Ошибка парсинга Amadeus:", e)

    return render(request, 'booking/flight_list.html', {
        'form': form,
        'flights': flights,
        'amadeus_flights': amadeus_flights,
        'popular_cities': popular_cities,
        'alternative_destinations': alternative_destinations,
        'search_performed': search_performed
    })

def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.flight = flight
            booking.save()
            for seat in generate_seat_numbers(booking.num_seats):
                Seat.objects.create(booking=booking, seat_number=seat)
            return render(request, 'booking/booking_success.html', {'booking': booking})
    else:
        form = BookingForm()
    return render(request, 'booking/booking_form.html', {'form': form, 'flight': flight})

@csrf_exempt
def amadeus_book_view(request):
    if request.method == "POST":
        today = timezone.now().date()
        errors = []

        def parse_date_safe(field, label, must_be_past=False, must_be_future=False, max_year=None):
            value = request.POST.get(field)
            try:
                dt = datetime.strptime(value, "%d.%m.%Y").date()
                if must_be_past and dt >= today:
                    errors.append(f"{label} должна быть в прошлом.")
                if must_be_future and dt <= today:
                    errors.append(f"{label} должна быть в будущем.")
                if max_year and dt.year > max_year:
                    errors.append(f"{label} не может быть позже {max_year} года.")
                return dt
            except Exception:
                errors.append(f"Неверный формат {label.lower()} (ДД.ММ.ГГГГ).")
                return None

        birth_date = parse_date_safe("birth_date", "Дата рождения", must_be_past=True)
        passport_expiry = parse_date_safe("passport_expiry", "Срок действия паспорта", must_be_future=True, max_year=2032)

        num_seats = int(request.POST.get("num_seats", 1))
        price_raw = request.POST.get("price", "").strip()
        print(price_raw)
        total_price = 0
        try:
            price = float(price_raw) if price_raw else 0.0
        except ValueError:
            errors.append("Некорректная цена.")
            price = 0.0
            total_price = round(price * num_seats, 2)

        booking_data = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "birth_date": birth_date,
            "gender": request.POST.get("gender"),
            "citizenship": request.POST.get("citizenship"),
            "passport_number": request.POST.get("passport_number"),
            "passport_expiry": passport_expiry,
            "passport_country": request.POST.get("passport_country"),
            "num_seats": num_seats,
            "departure_city": request.POST.get("departure"),
            "arrival_city": request.POST.get("arrival"),
            "price": price,
        }

        if errors:
            return render(request, "booking/booking_form_amadeus.html", {
                "departure": booking_data["departure_city"],
                "arrival": booking_data["arrival_city"],
                "price": booking_data["price"],
                "errors": errors,
                "form_data": request.POST,
                "total_price": total_price
            })

        booking = Booking.objects.create(**booking_data)

        for seat in generate_seat_numbers(booking.num_seats):
            Seat.objects.create(booking=booking, seat_number=seat)

        return render(request, "booking/booking_success_amadeus.html", {
            "name": f"{booking.first_name} {booking.last_name}",
            "email": booking.email,
            "departure": booking.departure_city,
            "arrival": booking.arrival_city,
            "price": booking.price,
            "num_seats": booking.num_seats,
            "total_price": total_price
        })

    return render(request, "booking/booking_form_amadeus.html", {
        "departure": request.GET.get("departure"),
        "arrival": request.GET.get("arrival"),
        "price": request.GET.get("price")
    })

def booking_history(request):
    bookings = Booking.objects.prefetch_related('seats').order_by('-created_at')
    for booking in bookings:
        seat_price = booking.flight.price if booking.flight else booking.price
        booking.total_price = seat_price * booking.num_seats

    return render(request, 'booking/booking_history.html', {
        'bookings': bookings
    })

def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.delete()
    return redirect('booking_history')

# def booking_form_amadeus(request):
#     return render(request, 'booking/booking_form_amadeus.html')

def booking_history(request):
    return render(request, 'booking/booking_history.html')

def booking_success_amadeus(request):
    data = request.session.get('booking_data', {})
    return render(request, 'booking/booking_success_amadeus.html', data)