from django.test import TestCase
from users.forms import LoginForm
from django import forms


class LoginFormTest(TestCase):
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
