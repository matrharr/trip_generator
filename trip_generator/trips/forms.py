from django import forms

class TripForm(forms.Form):
    destination = forms.CharField(label='Destination')
    departure_date = forms.CharField(label='Departure date')
    return_date = forms.CharField(label='Return date')
