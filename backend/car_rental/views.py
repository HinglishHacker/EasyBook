from django.shortcuts import render, redirect
from .forms import CarRentalForm
from django.utils.http import urlencode

def car_search(request):
    form = CarRentalForm(request.GET or None)
    if form.is_valid():
        data = form.cleaned_data
        pickup_location = data['pickup_location']
        dropoff_location = data['dropoff_location']
        pickup_date = data['pickup_date'].strftime('%Y-%m-%d')
        dropoff_date = data['dropoff_date'].strftime('%Y-%m-%d')
        car_type = data['car_type']

        url = (
            f"https://www.booking.com/car-rental/search.html"
            f"?pickup_location={pickup_location}"
            f"&dropoff_location={dropoff_location}"
            f"&pickup_date={pickup_date}"
            f"&dropoff_date={dropoff_date}"
            f"&group_car_type={car_type}"
        )
        return redirect(url)
    return render(request, 'car_rental/search.html', {'form': form})
