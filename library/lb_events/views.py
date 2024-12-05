from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic as views
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.contrib.auth import mixins as auth_mixin


from library.lb_events.forms import EventCreateForm
from library.lb_events.models import Event
from library.utils.save_functionality import toggle_saved_object


class EventCreateView(auth_mixin.LoginRequiredMixin, views.CreateView):
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


class EventListView(auth_mixin.LoginRequiredMixin, views.ListView):
    model = Event
    template_name = 'events/event_display.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_option = self.request.GET.get('filter', '')
        current_datetime = timezone.now()

        if filter_option == 'upcoming':
            queryset = queryset.filter(date__gte=current_datetime)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_upcoming'] = self.request.GET.get('filter', '')
        return context


class EventDetailView(auth_mixin.LoginRequiredMixin, views.DetailView):
    queryset = Event.objects.all()
    template_name = 'events/event_detail.html'


class EventEditView(auth_mixin.LoginRequiredMixin, views.UpdateView):
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
