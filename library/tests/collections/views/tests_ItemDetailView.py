import json

from django.urls import reverse

from library.lb_collections.models import Review
from tests.test_base import TestBase


class ItemDetailViewTests(TestBase):
    def test_get_item_detail__when_authorized_user__expect_200(self):
        self._create_user()
        self.client.login(**self.USER_DATA)

        item = self._create_item()

        expected_url = reverse('item detail', kwargs={'pk': item.pk, 'slug': item.slug})

        response = self.client.get(expected_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'collections/item_detail.html')
        self.assertIn('review_form', response.context)
        self.assertIn('reviews', response.context)

    def test_post_create_review__when_valid_comment_and_rating__expect_success(self):
        user = self._create_user()
        self.client.login(**self.USER_DATA)
        self._create_user_profile(user)

        item = self._create_item()

        detail_url = reverse('item detail', kwargs={'pk': item.pk, 'slug': item.slug})

        valid_data = {
            'comment': 'Amazing Item',
            'rating': 5,
        }

        response = self.client.post(detail_url, data=valid_data)

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['review_text'], 'Amazing Item')

        self.assertTrue(Review.objects.filter(user=user, item=item, comment='Amazing Item').exists())