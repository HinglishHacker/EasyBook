from django.db import models
from django.conf import settings

class Ticket(models.Model):
    origin = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    departutr_date = models.DateField(max_length=15)
    price = models.DecimalField(max_digits=8, decimal_places=2)

class Favourite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favourites'
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='favourited_by'
    )
    saved_at = models.DateTimeField(auto_now_add=True)

class Meta:
    unique_together = ('user', 'ticket')
    ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.email} — {self.ticket}"
    

