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
        self.assertIn("Hello!", html)

    def test_view_users_login_view_post(self):
        """Users application LoginView post method test
        Noe LoginView post method didn't return HttpResponse it return None
        """
        with self.assertRaises(ValueError):
            self.client.post("/users/login")
