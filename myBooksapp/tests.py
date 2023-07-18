from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.

class BookTestCase(TestCase):
    def setup(self):
        # Create new users
        self.valid_user = User.objects.create(
            username = "test_valid_user",
            password = "test_valid_password",
            email = "test_valid_email",
            first_name = " test_valid_first_name"
        )
        self.invalid_user = User.objects.create(
            username = "test_invalid_user",
            password = "test_invalid_password",
        )

        # Create client
        self.client = APIClient()

    def test_book_list(self):
        url = reverse("book-app:book-list")
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)
