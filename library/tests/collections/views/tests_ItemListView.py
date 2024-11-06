from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from library.lb_collections.models import Author, Item
from tests.helpers.image_creation import create_test_image

UserModel = get_user_model()


class ItemListViewTests(TestCase):
    def setUp(self):
        self.USER_DATA = {
            "email": "TestLibraryUser@library.com",
            "password": "BestLibraryEver123",
        }

        self.user = UserModel.objects.create_user(**self.USER_DATA)
        self.client.login(**self.USER_DATA)

        self.author = Author.objects.create(name="Author Test")
        self.item1 = Item.objects.create(
            title="Item 3",
            genre="Fiction",
            item_image=create_test_image(),
            item_type="Book",
            author=self.author,
            sample='Test Sample 1',
            publication_date=datetime.strptime("2020-11-20", "%Y-%m-%d").date(),
        )
        self.item2 = Item.objects.create(
            title="Item 1",
            genre="Fantasy",
            item_image=create_test_image(),
            item_type="Magazine",
            author=self.author,
            sample='Test Sample 2',
            publication_date=datetime.strptime("2020-10-20", "%Y-%m-%d").date(),
        )
        self.item3 = Item.objects.create(
            title="Item 2",
            genre="Fiction",
            item_image=create_test_image(),
            item_type="Book",
            author=self.author,
            sample='Test Sample 3',
            publication_date=datetime.strptime("2020-9-20", "%Y-%m-%d").date(),
        )

    def test_get_item_list_without_filters(self):
        response = self.client.get(reverse('item display'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'collections/item_display.html')
        self.assertEqual(len(response.context['items']), 3)

    def test_get_item_list_with_genre_filter(self):
        response = self.client.get(reverse('item display') + '?genre=Fiction')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'collections/item_display.html')
        self.assertEqual(len(response.context['items']), 2)
        for item in response.context['items']:
            self.assertEqual(item.genre, 'Fiction')

    def test_get_item_list_item_type_filter(self):
        response = self.client.get(reverse('item display') + '?item_type=Magazine')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['items']), 1)
        self.assertEqual(response.context['items'][0].item_type, 'Magazine')

    def test_get_item_list_both_filters(self):
        response = self.client.get(reverse('item display') + '?genre=Fiction&item_type=Book')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['items']), 2)
        for item in response.context['items']:
            self.assertEqual(item.genre, 'Fiction')
            self.assertEqual(item.item_type, 'Book')

    def test_context_data_in_item_list_view(self):
        response = self.client.get(reverse('item display'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('genre_query', response.context)
        self.assertIn('item_type_query', response.context)
        self.assertIn('item_choices', response.context)
        self.assertIn('items', response.context)