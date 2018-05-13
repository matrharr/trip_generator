from django.db import models


class Trip(models.Model):
    departure_date = models.DateField()
    return_date = models.DateField()


class Destination(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    city = models.CharField(max_length=128)
    country = models.CharField(max_length=128)


class Itinerary(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Flight(models.Model):
    departure_time = models.DateTimeField()
    return_time = models.DateTimeField()

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


class TripDay(models.Model):
    date = models.DateField()
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE)
    flight = models.ManyToManyField(Flight)
    accommodations = models.ManyToManyField(Accommodation)
    destinations = models.ManyToManyField(Destination)
