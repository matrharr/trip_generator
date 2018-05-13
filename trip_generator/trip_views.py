from django.views.generic.base import TemplateView
from django.shortcuts import redirect

from trip_generator import forms


class TripFormView(TemplateView):
    template_name = 'trips/trip_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.TripForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = forms.TripForm(self.request.POST)
        if form.is_valid():
            # foursquare api call for each destination
            # create ratio of days in place
            # for each day, make api call to get recommended
            # stay and flight if necessary
            return redirect('trips:itinerary')

        context['form'] = form
        return super().render_to_response(context=context)


class ItineraryView(TemplateView):
    template_name = 'trips/itinerary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
