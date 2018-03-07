from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone

from blog.forms import UserForm
from blog.models import Post


class HomeViewTests(TestCase):
    def setUp(self):
        url = reverse('blog:post_list')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_template_name(self):
        self.assertTemplateUsed('blog/post_list.html')


class PostTests(TestCase):
    def setUp(self):
        Post.objects.create(
            author_id=1,
            topic='Food',
            title='Healthy food',
            text='Test case post',
            published_date=timezone.now()
        )

    def test_post_detail_view_status_code(self):
        url = reverse('blog:post_detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_post_foodlist_view_status_code(self):
        url = reverse('blog:post_by_topic', kwargs={'topic': 'food'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_post_detail_view_not_found_status_code(self):
        url = reverse('blog:post_detail', kwargs={'pk': 15})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)


class SingUpTests(TestCase):
    def setUp(self):
        url = reverse('blog:signup')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        self.assertNotEquals(self.response.status_code, 404)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context_data.get('form')
        self.assertIsInstance(form, UserForm)

    def test_template_name(self):
        self.assertTemplateUsed('blog/sign_up.html')


class SuccessfulSignupTests(TestCase):
    def setUp(self):
        url = reverse('blog:signup')
        data = {
            'username': 'TestUser',
            'email': 'test@mail.com',
            'password': '123456789q'
        }

        self.response = self.client.post(url, data)
        self.home_url = reverse('blog:post_list')

    def test_response_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

