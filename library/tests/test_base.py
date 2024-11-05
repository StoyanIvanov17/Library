from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from library.lb_accounts.models import LibraryProfile
from library.lb_collections.models import Author, Item
from tests.helpers.image_creation import create_test_image

UserModel = get_user_model()


class TestBase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')

        self.USER_DATA = {
            "email": "TestLibraryUser@library.com",
            "password": "BestLibraryEver123",
        }

        self.ITEM_DATA = {
            "title": 'Test Title',
            "item_image": create_test_image(),
            "author": self.author,
            "genre": 'Test Genre',
            "item_type": 'Test Book',
            "sample": 'Test Sample',
            "publication_date": datetime.strptime("2020-11-20", "%Y-%m-%d").date(),
        }

        self.PROFILE_DATA = {
            "first_name": 'Test Name',
            "last_name": 'Test Last Name',
            "address": 'Test Address',
            "phone_number": '1234567890',
            "city": 'Test City'
        }

    def _create_user(self):
        return UserModel.objects.create_user(**self.USER_DATA)

    def _create_item(self):
        return Item.objects.create(**self.ITEM_DATA)

    def _create_user_profile(self, user):
        return LibraryProfile.objects.create(user=user, **self.PROFILE_DATA)