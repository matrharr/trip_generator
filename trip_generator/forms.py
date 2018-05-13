from datetime import date, timedelta

from django.forms import ModelForm, CharField, DateField, ValidationError, SelectDateWidget

from trip_generator.models import Trip

class TripForm(ModelForm):
    class Meta:
        model = Trip
        fields = ['departure_date', 'return_date']

    destinations = CharField(label='Destinations')
    departure_date = DateField(
        widget=SelectDateWidget,
        initial=date.today(),
    )
    return_date = DateField(
        widget=SelectDateWidget,
        initial=date.today() + timedelta(days=7),
    )

    def clean(self):
        cleaned_data = super().clean()
        destination_string = cleaned_data.get('destinations')
        departure_date = cleaned_data.get('departure_date')
        return_date = cleaned_data.get('return_date')

        if departure_date < date.today():
            raise ValidationError(
                'Departure date must be in the future.'
            )
        if departure_date > return_date:
            raise ValidationError(
                'Departure date must be before return date.'
            )

        delta = return_date - departure_date
        num_of_destinations = len(destination_string.split())

        if num_of_destinations >= delta.days:
            raise ValidationError(
                'Your trip must have more days than destinations.'
            )
