from django.test import TestCase
from django.urls import resolve
from users.views import LoginView, log_out


class UsersUrlTest(TestCase):
    def test_url_resolves_to_login_view(self):
        """User application '/users/login' pattern urls test
        Check '/users/login' pattern resolved class is LoginView
        """
        found = resolve("/users/login")
        self.assertEqual(found.func.view_class, LoginView)

    def test_url_resolves_to_user_log_out(self):
        """User application '/users/logout' pattern urls test
        Check '/users/logout' pattern resolved function is log_out
        """
        found = resolve("/users/logout")
        self.assertEqual(found.func, log_out)
