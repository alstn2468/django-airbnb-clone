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

    def test_login_form_clean_does_not_exist(self):
        """Users appliation login form clean method test
        Check LoginForm's user does not exist
        """
        form = LoginForm({"email": "error@test.com", "password": "testtest"})
        self.assertFalse(form.is_valid())
        self.assertIn("User does not exist", *form._errors.values())

    def test_login_form_clean_user_exist_password_wrong(self):
        """Users appliation login form clean method test
        Check LoginForm's password is wrong
        """
        form = LoginForm({"email": "test@test.com", "password": "wrong"})
        self.assertFalse(form.is_valid())
        self.assertIn("Password is wrong", *form._errors.values())

    def test_login_form_clean_is_valid_sucess(self):
        """Users appliation login form clean method test
        Check LoginForm's clean method return exist user data
        """
        user = {"email": "test@test.com", "password": "testtest"}
        form = LoginForm(user)

        if form.is_valid():
            self.assertEqual(user, form.clean())
