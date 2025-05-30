from django import forms

class HotelSearchForm(forms.Form):
    destination = forms.CharField(label='City or hotel', max_length=100)
    checkin = forms.DateField(label='Check-in day', widget=forms.DateInput(attrs={'type':'date'}))
    checkout = forms.DateField(label='Check-out day',widget=forms.DateInput(attrs={'type':'date'}))
    adults = forms.IntegerField(label='Взрослые', min_value=1, initial=2)
    children = forms.IntegerField(label='Дети', min_value=0, initial=0)