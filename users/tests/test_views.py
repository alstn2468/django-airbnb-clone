from django.test import TestCase
from users.models import User


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
