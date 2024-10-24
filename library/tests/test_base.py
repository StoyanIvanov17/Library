from django.contrib.auth import get_user_model
from django.test import TestCase

UserModel = get_user_model()


class TestBase(TestCase):
    USER_DATA = {
        "email": "TestLibraryUser@library.com",
        "password": "BestLibraryEver123",
    }

    def _create_user(self):
        return UserModel.objects.create_user(**self.USER_DATA)
