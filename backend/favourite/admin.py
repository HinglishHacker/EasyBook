from django.contrib import admin
from .models import Favourite

@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticket', 'saved_at')
    list_filter = ('saved_at',)
