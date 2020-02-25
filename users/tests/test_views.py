from django.test import TestCase


class UserViewTest(TestCase):
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

    def test_view_users_login_view_post(self):
        """Users application LoginView post method test
        Now LoginView post method didn't return HttpResponse it return None
        """
        with self.assertRaises(ValueError):
            self.client.post("/users/login")

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

