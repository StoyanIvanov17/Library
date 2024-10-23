from datetime import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse

from library.lb_collections.models import Item, Author
from tests.helpers.test_image_creation import create_test_image
from tests.test_base import TestBase

UserModel = get_user_model()


class BookCreateViewTests(TestBase):
    def setUp(self):
        self.user = self._create_user()
        self.client.login(**self.USER_DATA)
        item_image = create_test_image()
        self.ITEM_DATA = {
            "title": "Harry Potter",
            "item_image": item_image,
            "author": "J.K.Rowling",
            "genre": "Fantasy",
            "item_type": "book",
            "sample": "What an amazing book!",
            "publication_date": "2020-11-20",
        }

    def test_get_create__when_authorized_user__expect_200(self):
        response = self.client.get(reverse('item create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'collections/item_create.html')

    def test_get_create__when_unauthorized_user__expect_raise_403(self):
        self.client.logout()
        item_create_url = reverse('item create')
        login_url = reverse('signin user')

        response = self.client.get(item_create_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{login_url}?next={item_create_url}")

    def test_post_create__when_valid_data__expect_item_created(self):
        author = Author.objects.create(name='J.K.Rowling')
        item = Item.objects.create(
            title='Harry Potter',
            item_image=create_test_image(),
            author=author,
            genre='Fantasy',
            item_type='book',
            sample='What an amazing book!',
            publication_date=datetime.strptime("2020-11-20", "%Y-%m-%d").date(),
        )
        expected_url = reverse('item detail', kwargs={'pk': item.pk, 'slug': item.slug})

        response = self.client.get(reverse('item detail', kwargs={'pk': item.pk, 'slug': item.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], expected_url)
        self.assertTrue(Item.objects.filter(title=self.ITEM_DATA['title']).exists())

    def test_post_create__when_invalid_data__expect_form_errors(self):
        invalid_data = self.ITEM_DATA.copy()
        invalid_data['title'] = ''

        response = self.client.post(reverse('item create'), data=invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

        form = response.context['form']

        self.assertTrue(form.errors)
        self.assertIn('title', form.errors)
        self.assertEqual(form.errors['title'], ['This field is required.'])

