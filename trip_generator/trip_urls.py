from django.conf.urls import url
from trip_generator import trip_views


urlpatterns = [
    url(r'^$', trip_views.TripFormView.as_view(), name='trip_form'),
    url(r'^itinerary/(?P<itinerary_pk>\d+)', trip_views.ItineraryView.as_view(), name='itinerary')
]
