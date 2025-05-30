<<<<<<< HEAD
from django.shortcuts import render, redirect
from .forms import HotelSearchForm

def hotel_search(request):
    form = HotelSearchForm(request.GET or None)
    if form.is_valid():
        data = form.cleaned_data
        destination = data['destination']
        checkin = data['checkin'].strftime('%Y-%m-%d')
        checkout = data['checkout'].strftime('%Y-%m-%d')
        adults = data['adults']
        children = data['children']

        # Строим URL Booking.com
        booking_url = (
            f"https://www.booking.com/searchresults.ru.html?"
            f"ss={destination}"
            f"&checkin={checkin}"
            f"&checkout={checkout}"
            f"&group_adults={adults}"
            f"&group_children={children}"
            f"&no_rooms=1"
        )
        return redirect(booking_url)

    return render(request, 'hotels/hotel_search.html', {'form': form})
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> 317d9cb9eead09ebdceafcfddbee760a25846ecb
