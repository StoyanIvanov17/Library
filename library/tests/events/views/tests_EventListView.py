from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from library.lb_events.models import Event
from tests.helpers.test_image_creation import create_test_image


class EventListedViewTest(TestCase):

    def setUp(self):
        self.past_event = Event.objects.create(
            name="Past Event",
            date=timezone.now() - timezone.timedelta(days=10),
            time="10:00",
            location="Past Location",
            description="This is a past event",
            age_group='Adults',
            event_image=create_test_image(),
        )
        self.upcoming_event = Event.objects.create(
            name="Upcoming Event",
            date=timezone.now() + timezone.timedelta(days=10),
            time="14:00",
            location="Future Location",
            description="This is an upcoming event",
            age_group='Adults',
            event_image = create_test_image()
        )

    def test_view_with_no_filter(self):
        response = self.client.get(reverse('event display'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Past Event")
        self.assertContains(response, "Upcoming Event")
        self.assertEqual(len(response.context['events']), 2)

    def test_view_with_upcoming_filter(self):
        response = self.client.get(reverse('event display'), {'filter': 'upcoming'})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Past Event")
        self.assertContains(response, "Upcoming Event")
        self.assertEqual(len(response.context['events']), 1)

    def test_view_with_invalid_filter(self):
        response = self.client.get(reverse('event display'), {'filter': 'invalid'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Past Event")
        self.assertContains(response, "Upcoming Event")
        self.assertEqual(len(response.context['events']), 2)
