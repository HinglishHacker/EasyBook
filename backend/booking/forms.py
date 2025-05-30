from django import forms
from .models import Booking

class FlightSearchForm(forms.Form):
    departure_city = forms.CharField(label="Откуда")
    arrival_city = forms.CharField(label="Куда")
    departure_date = forms.DateField(label="Дата вылета", widget=forms.DateInput(attrs={'type': 'date'}))

class BookingForm(forms.ModelForm):
    email_confirm = forms.EmailField(label="Подтвердите Email")

    class Meta:
        model = Booking
        fields = [
            'email', 'email_confirm', 'phone', 'extra_phone',
            'first_name', 'last_name', 'birth_date', 'gender',
            'citizenship', 'passport_number', 'passport_expiry',
            'passport_country', 'num_seats'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'passport_expiry': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        confirm = cleaned_data.get("email_confirm")
        if email and confirm and email != confirm:
            self.add_error('email_confirm', "Email не совпадает.")
