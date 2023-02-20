from django.test import TestCase, Client
from django.urls import reverse
from yatube.urls import handler403, handler404


class ErrorTemplate(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_pages_error_uses_correct_template(self):
        templates_pages_names = {
            reverse(handler404): 'core/404.html',
            reverse(handler403): 'core/403csfr.html'
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
