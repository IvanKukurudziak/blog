from django.test import TestCase
from django.core.urlresolvers import reverse, resolve

from .forms import UserForm
from .views import SignupForm


class SingUpTest(TestCase):
    def setUp(self):
        url = reverse('blog:sign_up')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        self.assertNotEquals(self.response.status_code, 404)

    def test_url_resolve_signup_view(self):
        view = resolve('/sign_up')
        self.assertEquals(view.func, SignupForm.as_view)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertNotIsInstance(form, UserForm)
