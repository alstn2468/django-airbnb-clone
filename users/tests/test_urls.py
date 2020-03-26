from django.test import TestCase
from django.urls import resolve
from users.views import LoginView, log_out, SignUpView, complete_verification


class UsersUrlTest(TestCase):
    def test_url_resolves_to_login_view(self):
        """User application '/users/login' pattern urls test
        Check '/users/login' pattern resolved class is LoginView
        """
        found = resolve("/users/login")
        self.assertEqual(found.func.view_class, LoginView)

    def test_url_resolves_to_log_out(self):
        """User application '/users/logout' pattern urls test
        Check '/users/logout' pattern resolved function is log_out
        """
        found = resolve("/users/logout")
        self.assertEqual(found.func, log_out)

    def test_url_resolves_to_sign_up_view(self):
        """User application '/users/signup' pattern urls test
        Check '/users/signup' pattern resolved class is SignUpView
        """
        found = resolve("/users/signup")
        self.assertEqual(found.func.view_class, SignUpView)

    def test_url_resolves_to_complete_verification(self):
        """User application '/users/verify/<str:secret>' pattern urls test
        Check '/users/verify' pattern resolved function is complete_verification
        """
        found = resolve("/users/verify/secret")
        self.assertEqual(found.func, complete_verification)
