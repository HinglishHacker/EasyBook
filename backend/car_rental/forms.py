from django import forms

CAR_TYPE_CHOICE=[
    ('economy','Economy'),
    ('premium','Premium'),
    ('suv','Suv'),
    ('minivan','Minivan'),
    ('pickup','Pickup')
]

class CarRentalForm(forms.Form):
    pickup_location = forms.CharField(label='Pickup_location', max_length=100)
    dropoff_location = forms.CharField(label='Dropoff_location',max_length=100)
    pickup_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    dropoff_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    car_type = forms.ChoiceField(choices=CAR_TYPE_CHOICE)