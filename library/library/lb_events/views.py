from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic as views
from django.views.decorators.http import require_POST
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from library.lb_events.forms import EventCreateForm
from library.lb_events.models import Event
from library.utils.save_functionality import toggle_saved_object


class EventCreateView(views.CreateView):
    queryset = Event.objects.all()
    form_class = EventCreateForm
    template_name = 'events/event_create.html'

    def get_success_url(self):
        return reverse('event detail', kwargs={
            'pk': self.object.pk,
            'slug': self.object.slug
        })

    def get_form(self, form_class=form_class):
        form = super().get_form(form_class=form_class)

        form.instance.user = self.request.user
        return form


def events_listed(request):
    events = Event.objects.all()
    current_datetime = timezone.now()
    filter_option = request.GET.get('filter', '')

    if filter_option == 'upcoming':
        events = events.filter(date__gte=current_datetime)

    context = {
        'events': events,
        'filter_upcoming': filter_option,
    }

    return render(request, 'events/event_display.html', context)


class EventDetailView(views.DetailView):
    queryset = Event.objects.all()
    template_name = 'events/event_detail.html'


class EventEditView(views.UpdateView):
    queryset = Event.objects.all()
    template_name = 'events/event_update.html'
    form_class = EventCreateForm

    def get_success_url(self):
        return reverse('event detail', kwargs={
            'pk': self.object.pk,
            'slug': self.object.slug
        })


class EventDeleteView(views.DeleteView):
    queryset = Event.objects.all()
    success_url = reverse_lazy('event display')


class SaveEventAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, slug):
        try:
            user_profile = request.user.libraryprofile
            favorited = toggle_saved_object(user_profile, Event, 'saved_events', pk)

            return JsonResponse({'favorited': favorited})

        except Event.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Event not found.'}, status=404)
