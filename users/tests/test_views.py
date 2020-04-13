from django.test import TestCase
from users.models import User
from unittest import mock


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

    if args[0] == "https://github.com/login/oauth/access_token":
        return MockResponse({"code": "testcode"}, 200)


class UserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running UserViewTest
        Create one test user has email
        """
        User.objects.create_user(username="test@test.com", password="testtest")

    def test_view_users_login_view_get(self):
        """Users application LoginView get method test
        Check LoginView HttpResponse content data contain right data
        """
        response = self.client.get("/users/login")
        html = response.content.decode("utf8")

        self.assertEqual(200, response.status_code)
        self.assertIn("<title>Log In | Airbnb</title>", html)
        self.assertIn('<input type="email" name="email" required id="id_email">', html)
        self.assertIn(
            '<input type="password" name="password" required id="id_password">', html
        )

    def test_view_users_login_view_post_login_success(self):
        """Users application LoginView post method test
        Check redirect home when success login process
        """
        data = {"email": "test@test.com", "password": "testtest"}
        response = self.client.post("/users/login", data)

        self.assertEqual(302, response.status_code)

        response = self.client.get("")

        html = response.content.decode("utf8")
        self.assertIn('<a href="/users/logout">Logout</a>', html)

    def test_view_users_login_view_post_login_fail(self):
        """Users application LoginView post method test
        Check render login template when fail login process
        """
        data = {"email": "test@test.com", "password": "test"}
        response = self.client.post("/users/login", data)
        html = response.content.decode("utf8")

        self.assertEqual(200, response.status_code)
        self.assertIn("<title>Log In | Airbnb</title>", html)

    def test_view_users_login_view_csrf_token(self):
        """Users application LoginView csrf_token test
        Check csrf_token hidden input is in login form
        """
        response = self.client.get("/users/login")
        html = response.content.decode("utf8")
        csrf_token = response.context.get("csrf_token")

        self.assertIn(
            f'<input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">',
            html,
        )

    def test_view_users_login_view_post_log_out(self):
        """Users application log_out post method test
        Check success logout redirect core:home
        """
        data = {"email": "test@test.com", "password": "testtest"}
        response = self.client.post("/users/login", data)
        response = self.client.post("/users/logout")

        self.assertEqual(302, response.status_code)

        response = self.client.get("")
        html = response.content.decode("utf8")
        self.assertIn('<a href="/users/login">Login</a>', html)
        self.assertIn('<a href="/users/signup">Sign up</a>', html)

    def test_view_users_sign_up_view_get(self):
        """Users application SignUpView test
        Check SignUpView HttpResponse content data contain right data
        """
        response = self.client.get("/users/signup")
        html = response.content.decode("utf8")

        self.assertEqual(200, response.status_code)
        self.assertIn("<title>Sign Up | Airbnb</title>", html)
        self.assertIn(
            '<input type="text" name="first_name"', html,
        )
        self.assertIn(
            '<input type="text" name="last_name"', html,
        )
        self.assertIn('<input type="email" name="email"', html)
        self.assertIn(
            '<input type="password" name="password" required id="id_password">', html
        )
        self.assertIn(
            '<input type="password" name="password_check" required id="id_password_check">',
            html,
        )

    def test_view_users_sign_up_view_post_success(self):
        """Users application sign up view post method test
        Check success create user and login then redirect home
        """
        data = {
            "first_name": "test",
            "last_name": "test",
            "email": "testtest@test.com",
            "password": "testtest",
            "password_check": "testtest",
        }
        response = self.client.post("/users/signup", data)

        self.assertEqual(302, response.status_code)

        response = self.client.get("")
        html = response.content.decode("utf8")

        self.assertIn('<a href="/users/logout">Logout</a>', html)
        self.assertIsNotNone(User.objects.get(username="testtest@test.com"))

    def test_view_users_sign_up_view_post_fail(self):
        """Users application sign up view post method test
        Check fail to create user and raise four ValidationError
        """
        data = {
            "email": "test@test.com",
            "password": "testtest",
            "password_check": "test",
        }
        response = self.client.post("/users/signup", data)
        html = response.content.decode("utf8")

        self.assertEqual(2, html.count("errorlist"))

    def test_complete_verification_success(self):
        """Users application complete_verifiation view success test
        Check user object's email_verified field is changed to True
        """
        user = User.objects.get(username="test@test.com")
        with mock.patch("uuid.uuid4") as uuid4:
            uuid4.return_value = mock.Mock(hex="a" * 20)
            self.assertTrue(User.verify_email(user))

        user = User.objects.get(email_secret="a" * 20)
        self.assertFalse(user.email_verified)

        response = self.client.post(f"/users/verify/{'a' * 20}")
        self.assertEqual(302, response.status_code)

        user = User.objects.get(username="test@test.com")
        self.assertTrue(user.email_verified)
        self.assertEqual("", user.email_secret)

    def test_complete_verification_fail(self):
        """Users application complete_verifiation view fail test
        Check complete_verification raise DoesNotExist exception
        """
        with self.assertRaises(User.DoesNotExist):
            response = self.client.post(f"/users/verify/{'b' * 20}")
            self.assertEqual(302, response.status_code)
            self.assertIsNone(User.objects.get(email_secret="b" * 20))

    def test_github_login(self):
        """Users application github_login view test
        Check github_login redirect to Authorization callback url
        """
        response = self.client.get("/users/login/github")
        self.assertEqual(302, response.status_code)

    def test_github_callback_code_is_none(self):
        """Users application github_callback view not has code test
        Check github_callback redirect to home
        """
        response = self.client.get("/users/login/github/callback")
        self.assertEqual(302, response.status_code)

    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_github_callback_code_is_not_none(self, mock_get):
        """Users application github_callback view has code test
        Check github_callback redirect to home
        """
        response = self.client.get("/users/login/github/callback?code=testtest")
        self.assertEqual(302, response.status_code)
