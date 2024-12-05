from django.contrib.auth import get_user_model
from django.urls import reverse

from library.lb_collections.models import Item
from tests.test_base import TestBase

UserModel = get_user_model()


class ItemCreateViewTests(TestBase):
    def test_get_create__when_authorized_user__expect_200_and_correct_template(self):
        self._create_user()
        self.client.login(**self.USER_DATA)

        response = self.client.get(reverse('item create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'collections/item_create.html')

    def test_get_create__when_unauthorized_user__expect_302_redirect_to_login(self):
        item_create_url = reverse('item create')
        login_url = reverse('signin user')

        response = self.client.get(item_create_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{login_url}?next={item_create_url}"
        )

    def test_post_create__when_valid_data__expect_item_created(self):
        item = self._create_item()
        expected_url = reverse('item detail', kwargs={'pk': item.pk, 'slug': item.slug})

        response = self.client.get(expected_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.request['PATH_INFO'], expected_url)
        self.assertTrue(Item.objects.filter(title=item.title).exists())

    def test_post_create__when_invalid_data__expect_form_errors(self):
        self._create_user()
        self.client.login(**self.USER_DATA)

        invalid_data = self.ITEM_DATA.copy()
        invalid_data['title'] = ''

        response = self.client.post(reverse('item create'), data=invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']

        self.assertTrue(form.errors)
        self.assertIn('title', form.errors)
        self.assertEqual(form.errors['title'], ['This field is required.'])


