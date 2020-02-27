from django.test import TestCase
from users.forms import LoginForm
from users.models import User
from django import forms


class LoginFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running UserModelTest
        Create one test user has email
        """
        User.objects.create_user(username="test@test.com", password="testtest")

    def test_login_form_email_field(self):
        """Users application login form email field test
        Check LoginForm email field set up is right
        """
        form = LoginForm()
        self.assertTrue(form.fields["email"].__class__.__name__ == "EmailField")
        self.assertTrue(form.fields["email"].required)

    def test_login_form_password_field(self):
        """Users application login form password field test
        Check LoginForm password field set up is right
        """
        form = LoginForm()
        self.assertTrue(form.fields["password"].__class__.__name__ == "CharField")
        self.assertTrue(form.fields["password"].required)
        self.assertIsInstance(form.fields["password"].widget, forms.PasswordInput)

    def test_login_form_clean_email_is_exist(self):
        """Users appliation login form clean_email method test
        Check LoginForm email data user is exist
        """
        form = LoginForm({"email": "test@test.com", "password": "testtest"})

        if form.is_valid():
            self.assertEqual(form.clean_email(), "test@test.com")

    def test_login_form_clean_password_true(self):
        """Users appliation login form clean_password method test
        Check LoginForm clean_password method return None
        """
        form = LoginForm()
        self.assertIsNone(form.clean_password())

    def test_login_form_clean_email_does_not_exist(self):
        """Users appliation login form clean_email method test
        Check user does not exist and for is invalid
        """
        form = LoginForm({"email": "error@test.com", "password": "testtest"})
        self.assertFalse(form.is_valid())
