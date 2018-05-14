import json
import requests

from django.views.generic.base import TemplateView
from django.shortcuts import redirect

from trip_generator import forms
from trip_generator.models import Destination, Itinerary


class TripFormView(TemplateView):
    template_name = 'trips/trip_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.TripForm()
        return context

    def post(self, request, *args, **kwargs):
        form = forms.TripForm(self.request.POST)

        if form.is_valid():
            form.save()
            destination_one = form.cleaned_data['destination_one']
            destination_two = form.cleaned_data['destination_two']
            destinations_three = form.cleaned_data['destination_three']

            destinations = [
                destination_one,
                destination_two,
                destinations_three,
            ]

            departure_date = form.cleaned_data['departure_date']
            return_date = form.cleaned_data['return_date']
            trip = form.instance

            self.__create_destinations(destinations, trip)

            itinerary = self.__create_itinerary(
                trip, departure_date, return_date
            )

            return redirect('trips:itinerary', itinerary_pk=itinerary.pk)

        context['form'] = form
        return super().render_to_response(context=context)

    def __create_destinations(self, destinations, trip):
        url = ''

        destination_objects = []
        for dest in destinations:
            # get lat/long for each destination
            dest_obj = Destination.objects.create_destination(
                location_input=dest,
                trip=trip,
            )

            params = dict(
              client_id='',
              client_secret='',
              v='20180323',
              ll='{},{}'.format(dest_obj.latitude, dest_obj.longitude),
              query='coffee',
              # limit=1
            )
            resp = requests.get(url=url, params=params)
            data = json.loads(resp.text)
            dest_obj.number_of_attractions = len(data['response']['venues'])
            dest_obj.save()
            destination_objects.append(dest_obj)

        Destination.create_trip_day_ratio(destination_objects)

    def __create_itinerary(self, trip, departure_date, return_date):
        itinerary = Itinerary.objects.create(trip=trip)
        itinerary.generate()
        return itinerary


class ItineraryView(TemplateView):
    template_name = 'trips/itinerary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
