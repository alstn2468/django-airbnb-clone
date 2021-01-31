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
            login_method=User.LOGIN_EMAIL,
        )
        User.objects.create_user(
            username="kakao@kakao.com",
            email="kakao@kakao.com",
            password="testtest",
            login_method=User.LOGIN_KAKAO,
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
        login = self.client.login(username="test@test.com", password="testtest")

        self.assertTrue(login)

        response = self.client.get("/users/login")
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse("core:home"), response.url)

    def test_email_login_only_view_sucess(self):
        """User application EmailLoginOnlyView success test
        Can access update password page with email logged in user
        """
        login = self.client.login(username="test@test.com", password="testtest")
        self.assertTrue(login)

        response = self.client.get("/users/update-password")
        self.assertEqual(200, response.status_code)

    def test_email_login_only_view_fail(self):
        """User application EmailLoginOnlyView fail test
        Can access update password page with kakoa logged in user
        """
        login = self.client.login(username="kakao@kakao.com", password="testtest")
        self.assertTrue(login)

        response = self.client.get("/users/update-password")
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse("core:home"), response.url)
