from datetime import datetime

from django.urls import reverse

from library.lb_collections.models import Item, Author
from tests.helpers.test_image_creation import create_test_image
from tests.test_base import TestBase


class BookDetailViewTests(TestBase):
    def setUp(self):
        self.user = self._create_user()
        self.client.login(**self.USER_DATA)
        item_image = create_test_image()
        author = Author.objects.create(
            name='J.K.Rowling'
        )
        self.item = Item.objects.create(
            title="Harry Potter",
            item_image=item_image,
            author=author,
            genre="Fantasy",
            item_type="book",
            sample="What an amazing book!",
            publication_date=datetime.strptime(
                "2020-11-20",
                "%Y-%m-%d"
            ),
        )
        self.review_data = {
            "comment": "This is a great book!"
        }
        self.url = reverse(
            'item detail',
            kwargs={
                'pk': self.item.pk,
                'slug': self.item.slug
            }
        )

    def test_get_item_detail__when_authorized_user__expect_200(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'collections/item_detail.html')
        self.assertIn('review_form', response.context)
        self.assertIn('reviews', response.context)

    def test_get_item_detail__when_unauthorized_user__expect_raise_403(self):
        self.client.logout()
        login_url = reverse('signin user')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{login_url}?next={self.url}")