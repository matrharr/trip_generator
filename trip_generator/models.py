import json
import requests

from django.db import models


class Trip(models.Model):
    starting_location = models.CharField(max_length=128)
    departure_date = models.DateField()
    return_date = models.DateField()
    number_of_days = models.IntegerField(
        default=None,
        blank=True,
        null=True,
    )


class DestinationManager(models.Manager):
    def create_destination(self, location_input, trip):
        lat, lng = self.__get_lat_lon(location_input)
        # country = self.__get_country(city)
        destination = self.create(
            # city=city,
            # country=country,
            trip=trip,
            latitude=lat,
            longitude=lng,
        )
        return destination

    def __get_lat_lon(self, location_input):
        key = ''
        base = ''
        query = 'address=' + location_input
        url = base + query + '&key=' + key
        res = requests.get(url=url)
        content = json.loads(res._content.decode())
        lat = content['results'][0]['geometry']['location']['lat']
        lng = content['results'][0]['geometry']['location']['lng']

        return lat, lng


class Destination(models.Model):
    objects = DestinationManager()

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    city = models.CharField(max_length=128)
    country = models.CharField(max_length=128)

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        default=None,
        blank=True,
        null=True,
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        default=None,
        blank=True,
        null=True,
    )

    number_of_attractions = models.IntegerField(
        default=None,
        blank=True,
        null=True,
    )

    trip_day_percentage = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        default=None,
        blank=True,
        null=True,
    )

    days_at_destination = models.IntegerField(
        default=None,
        blank=True,
        null=True,
    )

    @classmethod
    def create_trip_day_ratio(cls, destinations):
        total_attractions = \
            sum(dest.number_of_attractions for dest in destinations)
        for dest in destinations:
            percentage = dest.number_of_attractions/total_attractions
            dest.trip_day_percentage = percentage
            dest.save()

    def set_days_at_destination(self, total_number_of_days):
        days_at_destination = round(num_of_days * dest.trip_day_percentage)
        dest.days_at_destination = days_at_destination
        dest.save()


class Itinerary(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Flight(models.Model):
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    origin = models.CharField(max_length=128)
    destination = models.CharField(max_length=128)

    price = models.DecimalField(max_digits=50, decimal_places=2)


class Accommodation(models.Model):
    address = models.CharField(max_length=128)

    price = models.DecimalField(max_digits=50, decimal_places=2)

    check_in_datetime = models.DateTimeField()
    check_out_datetime = models.DateTimeField()

    city = models.CharField(max_length=128)
    country = models.CharField(max_length=128)


class ItineraryDay(models.Model):
    date = models.DateField()

    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE)
    flight = models.ManyToManyField(Flight)
    accommodations = models.ManyToManyField(Accommodation)
    destinations = models.ManyToManyField(Destination)
