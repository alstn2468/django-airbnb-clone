from django.test import TestCase
from django.shortcuts import reverse
from users.models import User
from unittest import mock


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_requests_token(*args, **kwargs):
    if args[0] == "https://github.com/login/oauth/access_token":
        return MockResponse({"access_token": "test_access_token"}, 200)

    elif args[0] == "https://kauth.kakao.com/oauth/token":
        return MockResponse({"access_token": "test_access_token"}, 200)


def mocked_requests_exist_oauth_profile(*args, **kwargs):
    if args[0] == "https://api.github.com/user":
        return MockResponse(
            {
                "login": "test_user",
                "name": "test_user",
                "email": "test@test.com",
                "bio": "this is test user",
            },
            200,
        )


def mocked_requests_noneexist_profile(*args, **kwargs):
    if args[0] == "https://api.github.com/user":
        return MockResponse(
            {
                "login": "test",
                "name": "test",
                "email": "testtest@test.com",
                "bio": "this is test user",
            },
            200,
        )


def mocked_requests_exist_not_oauth_profile(*args, **kwargs):
    if args[0] == "https://api.github.com/user":
        return MockResponse(
            {
                "login": "kakao_user",
                "name": "kakao_user",
                "email": "kakao@kakao.com",
                "bio": "this is kakao user",
            },
            200,
        )


def mocked_requests_no_login(*args, **kwargs):
    if args[0] == "https://api.github.com/user":
        return MockResponse({}, 200)


def mocked_requests_error(*args, **kwargs):
    if args[0] == "https://github.com/login/oauth/access_token":
        return MockResponse({"error": "error"}, 200)

    elif args[0] == "https://kauth.kakao.com/oauth/token":
        return MockResponse({"error": "error"}, 200)


class UserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running UserViewTest
        Create one test user has email
        """
        User.objects.create_user(
            username="test@test.com",
            email="test@test.com",
            password="testtest",
            login_method=User.LOGIN_GITHUB,
        )
        User.objects.create_user(
            username="kakao@kakao.com",
            email="kakao@kakao.com",
            bio="this is kakao user",
            first_name="kakao_user",
            login_method=User.LOGIN_KAKAO,
        )

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
        """Users application complete_verification view fail test
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
        self.assertIn("https://github.com/login/oauth/authorize", response.url)

    def test_github_callback_code_is_none(self):
        """Users application github_callback view not has code test
        Check github_callback redirect to login when code is None
        """
        response = self.client.get("/users/login/github/callback")
        self.assertEqual(302, response.status_code)
        self.assertEqual(response.url, reverse("users:login"))

    @mock.patch("requests.post", side_effect=mocked_requests_error)
    def test_github_callback_has_error(self, mock_get):
        """Users application github_callback view has error test
        Check github_callback redirect to login when has error at token_json
        """
        response = self.client.get("/users/login/github/callback?code=testtest")
        self.assertEqual(302, response.status_code)
        self.assertEqual(response.url, reverse("users:login"))

    @mock.patch("requests.post", side_effect=mocked_requests_token)
    @mock.patch("requests.get", side_effect=mocked_requests_no_login)
    def test_github_callback_is_no_username(self, mock_post, mock_get):
        """Users application github_callback view username is None
        Check github_callback redirect to login when username is None
        """
        response = self.client.get("/users/login/github/callback?code=testtest")
        self.assertEqual(302, response.status_code)
        self.assertEqual(response.url, reverse("users:login"))

    @mock.patch("requests.post", side_effect=mocked_requests_token)
    @mock.patch("requests.get", side_effect=mocked_requests_noneexist_profile)
    def test_github_callback_noneexist_github_profile(self, mock_post, mock_get):
        """Users application github_callback view hasn't user profile test
        Check github_callback create user with login and redirect to home
        """
        response = self.client.get("/users/login/github/callback?code=testtest")
        self.assertEqual(302, response.status_code)
        self.assertEqual(response.url, reverse("core:home"))

        user = User.objects.get(username="testtest@test.com")

        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, "test")
        self.assertEqual(user.bio, "this is test user")
        self.assertEqual(user.email, "testtest@test.com")
        self.assertEqual(user.login_method, User.LOGIN_GITHUB)

        response = self.client.get("/")
        self.assertEqual(response.context[0]["user"], user)

    @mock.patch("requests.post", side_effect=mocked_requests_token)
    @mock.patch("requests.get", side_effect=mocked_requests_exist_not_oauth_profile)
    def test_github_callback_not_github_profile(self, mock_post, mock_get):
        """Users application github_callback view user's login method test
        Check github_callback redirect to login when user's login method not Github
        """
        response = self.client.get("/users/login/github/callback?code=testtest")
        self.assertEqual(302, response.status_code)
        self.assertEqual(response.url, reverse("users:login"))

    @mock.patch("requests.post", side_effect=mocked_requests_token)
    @mock.patch("requests.get", side_effect=mocked_requests_exist_oauth_profile)
    def test_github_callback_exist_github_profile(self, mock_post, mock_get):
        """Users application github_callback view has user profile test
        Check github_callback redirect to home when already have an account
        """
        response = self.client.get("/users/login/github/callback?code=testtest")
        self.assertEqual(302, response.status_code)
        self.assertEqual(response.url, reverse("core:home"))

        user = User.objects.get(username="test@test.com")

        response = self.client.get("/")
        self.assertEqual(response.context[0]["user"], user)

    def test_kakao_login(self):
        """Users application kakao_login view test
        Check kakao_login redirect to Authorization callback url
        """
        response = self.client.get("/users/login/kakao")
        self.assertEqual(302, response.status_code)
        self.assertIn("https://kauth.kakao.com/oauth/authorize", response.url)

    def test_kakao_callback_code_is_none(self):
        """Users application kakao_callback view not has code test
        Check kakao_callback redirect to login when code is None
        """
        response = self.client.get("/users/login/kakao/callback")
        self.assertEqual(302, response.status_code)
        self.assertEqual(response.url, reverse("users:login"))

    @mock.patch("requests.post", side_effect=mocked_requests_token)
    def test_kakao_callback_code_is_not_none(self, mock_post):
        """Users application kakao_callback view has code test
        Check kakao_callback redirect to home when code is not None
        """
        response = self.client.get("/users/login/kakao/callback?code=testtest")
        self.assertEqual(302, response.status_code)
        self.assertEqual(response.url, reverse("core:home"))

    @mock.patch("requests.post", side_effect=mocked_requests_error)
    def test_kakao_callback_has_error(self, mock_get):
        """Users application kakao_callback view has error test
        Check kakao_callback redirect to login when has error at token_json
        """
        response = self.client.get("/users/login/kakao/callback?code=testtest")
        self.assertEqual(302, response.status_code)
        self.assertEqual(response.url, reverse("users:login"))
