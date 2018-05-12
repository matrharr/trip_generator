from django.conf.urls import url
from trip_generator.trips import views


urlpatterns = [
    url(r'^$', views.TripFormView.as_view(), name='trip_form'),
    url(r'^itinerary', views.ItineraryView.as_view(), name='itinerary')
]
