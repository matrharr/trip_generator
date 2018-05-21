import json
import requests
from datetime import timedelta

from django.views.generic.base import TemplateView
from django.shortcuts import redirect

from django.conf import settings

from trip_generator import forms
from trip_generator.models import Destination, Itinerary, ItineraryDay, Flight


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

            itinerary = self.__create_itinerary(trip)

            return redirect('trips:itinerary', itinerary_pk=itinerary.pk)
        context = {}
        context['form'] = form
        return super().render_to_response(context=context)

    def __create_destinations(self, destinations, trip):
        url = 'https://api.foursquare.com/v2/venues/search'

        destination_objects = []
        for dest in destinations:
            # get lat/long for each destination
            dest_obj = Destination.objects.create_destination(
                location_input=dest,
                trip=trip,
            )

            params = dict(
              client_id=settings.FOURSQUARE_CLI_ID,
              client_secret=settings.FOURSQUARE_CLI_SECRET,
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

    def __create_itinerary(self, trip):
        itinerary = Itinerary.objects.create(trip=trip)

        self.__create_itinerary_days(itinerary)

        return itinerary

    def __create_itinerary_days(self, itinerary):
        trip = itinerary.trip
        num_of_days = trip.number_of_days
        day = 1
        destinations = trip.destination_set.get_queryset()
        dest_list = []

        for dest in destinations:
            dest.set_days_at_destination(num_of_days)
            dest_list.append(dest)

        current_destination = dest_list.pop()

        while day <= num_of_days:
            date = trip.departure_date + timedelta(days=day)
            itinerary_day = ItineraryDay.objects.create(
                date=date,
                itinerary=itinerary,
            )

            itinerary_day.destinations.add(current_destination)


            # TODO: get accommodation

            # get flight to next, or flight to finish
            if day == current_destination.days_at_destination and len(destinations) > 0:
                # get flight to next destination
                departure_location = current_destination
                current_destination = dest_list.pop()

                self.__get_flight(
                    itinerary_day,
                    departure_location,
                    current_destination,
                )

            elif len(destinations) == 0:
                # get return flight
                self.__get_flight(
                    itinerary_day,
                    current_destination,
                    trip.starting_location,
                )

            day += 1

    def __get_flight(self, itinerary_day, origin, destination):
        response_flight = {
            'departure_time': itinerary_day.date + timedelta(days=10),
            'arrival_time': itinerary_day.date + timedelta(days=11),
            'origin': origin,
            'destination': destination,
            'price': 800,
        }

        flight = Flight.objects.create(
            departure_time=response_flight['departure_time'],
            arrival_time=response_flight['arrival_time'],
            origin=response_flight['origin'],
            destination=response_flight['destination'],
            price=response_flight['price'],
        )

        itinerary_day.flight.add(flight)
        itinerary_day.save()


class ItineraryView(TemplateView):
    template_name = 'trips/itinerary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itinerary_pk = kwargs['itinerary_pk']
        itinerary = Itinerary.objects.get(pk=itinerary_pk)
        context['itinerary'] = itinerary
        context['itinerary_days'] = itinerary.itineraryday_set.get_queryset()

        return context
