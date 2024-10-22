from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from library.lb_collections.models import Item

UserModel = get_user_model()


class BookCreateViewTests(TestCase):
    USER_DATA = {
        "email": "TestLibraryUser@library.com",
        "password": "BestLibraryEver123",
    }

    ITEM_DATA = {
        "title": "TestPet",
        "item_image": "item_images/5_wct9Ui1.jpg",
        "author": "J.K.Rowling",
        "genre": "Fantasy",
        "item_type": "Book",
        "sample": "What an amazing book!",
        "publication_date": "2020-11-20",
    }

    def create_valid_item(self):
        user = self._create_user()
        item = Item(
            title=self.ITEM_DATA['title'],
            item_image=self.ITEM_DATA['item_image'],
            author=self.ITEM_DATA['author'],
            genre=self.ITEM_DATA['genre'],
            item_type=self.ITEM_DATA['item_type'],
            sample=self.ITEM_DATA['sample'],
            publication_date=self.ITEM_DATA['publication_date'],
            user=user,
        )
        item.save()
        return item

    def _create_user(self):
        return UserModel.objects.create_user(**self.USER_DATA)

    def test_get_create__when_authorized_user__expect_200(self):
        self._create_user()
        self.client.login(**self.USER_DATA)

        response = self.client.get(reverse('item create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'collections/item_create.html')

    def test_get_create__when_unauthorized_user__expect_raise_403(self):
        item_create_url = reverse('item create')
        login_url = reverse('signin user')

        response = self.client.get(reverse('item create'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{login_url}?next={item_create_url}"
        )
    