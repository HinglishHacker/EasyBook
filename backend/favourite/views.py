from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Favourite
from .models import Ticket


@login_required
def add_to_favourites(request,ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    Favourite.objects.get_or_create(user=request.user, ticket=ticket)
    return redirect('favourite_list')

@login_required
def remove_from_favourites(request,ticket_id):
    Favourite.objects.filter(user=request.user, ticket_id=ticket_id).delete()
    return redirect('favourite_list')

@login_required
def favourite_list(request):
    favourites = Favourite.objects.filter(user=request.user).select_related('ticket')
    return render(request, 'favourites/favourite_list.html', {'favourites': favourites}) 

