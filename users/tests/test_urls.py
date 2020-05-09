from django.test import TestCase
from django.urls import resolve
from users.views import (
    LoginView,
    log_out,
    SignUpView,
    complete_verification,
    github_login,
    github_callback,
    kakao_login,
    kakao_callback,
)


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

    def test_url_resolves_to_github_login(self):
        """User applictaion '/users/login/github' pattern urls test
        Check '/users/login/github' pattern resolved function is github_login
        """
        found = resolve("/users/login/github")
        self.assertEqual(found.func, github_login)

    def test_url_resolves_to_github_callback(self):
        """User applictaion '/users/login/github/callback' pattern urls test
        Check '/users/login/github/callback' pattern resolved function is github_callback
        """
        found = resolve("/users/login/github/callback")
        self.assertEqual(found.func, github_callback)

    def test_url_resolves_to_kakao_login(self):
        """User applictaion '/users/login/kakao' pattern urls test
        Check '/users/login/kakao' pattern resolved function is kakao_login
        """
        found = resolve("/users/login/kakao")
        self.assertEqual(found.func, kakao_login)

    def test_url_resolves_to_kakao_callback(self):
        """User applictaion '/users/login/kakao/callback' pattern urls test
        Check '/users/login/kakao/callback' pattern resolved function is kakao_callback
        """
        found = resolve("/users/login/kakao/callback")
        self.assertEqual(found.func, kakao_callback)
