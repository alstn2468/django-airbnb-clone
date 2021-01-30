from django.shortcuts import reverse
from django.test import TestCase
from users.models import User


class UserMixinsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running UserMixinsTest
        Create one test user has email
        """
        User.objects.create_user(
            username="test@test.com",
            email="test@test.com",
            password="testtest",
            first_name="test",
            login_method=User.LOGIN_EMAIL,
        )

    def test_logged_out_only_view_sucess(self):
        """User application LoggedOutOnlyView success test
        Can access login page when isn't logged in
        """
        response = self.client.get("/users/login")
        self.assertEqual(200, response.status_code)

    def test_logged_out_only_view_no_permission(self):
        """User application LoggedOutOnlyView no permission test
        Can't access login page and redirected to home when logged in
        """
        data = {"email": "test@test.com", "password": "testtest"}
        response = self.client.post("/users/login", data)
        self.assertEqual(302, response.status_code)

        response = self.client.get("/users/login")
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse("core:home"), response.url)