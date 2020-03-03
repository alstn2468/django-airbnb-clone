from django.test import TestCase
from users.forms import LoginForm, SignUpForm
from users.models import User
from django import forms


class LoginFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running LoginFormTest
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
        """Users appliation login form clean method fail test
        Check LoginForm's user does not exist
        """
        form = LoginForm({"email": "error@test.com", "password": "testtest"})
        self.assertFalse(form.is_valid())
        self.assertIn("User does not exist", *form._errors.values())

    def test_login_form_clean_user_exist_password_wrong(self):
        """Users appliation login form clean method fail test
        Check LoginForm's password is wrong
        """
        form = LoginForm({"email": "test@test.com", "password": "wrong"})
        self.assertFalse(form.is_valid())
        self.assertIn("Password is wrong", *form._errors.values())

    def test_login_form_clean_is_valid_sucess(self):
        """Users appliation login form clean method success test
        Check LoginForm's clean method return exist user data
        """
        user = {"email": "test@test.com", "password": "testtest"}
        form = LoginForm(user)

        if form.is_valid():
            self.assertEqual(user, form.clean())


class SignUpFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running SignUpFormTest
        """
        pass

    def test_sign_up_form_first_name_fields(self):
        """User application sign up form first name fields test
        Check SignUpForm first_name field set up is right
        """
        form = SignUpForm()
        self.assertTrue(form.fields["first_name"].__class__.__name__ == "CharField")
        self.assertTrue(form.fields["first_name"].required)
        self.assertTrue(form.fields["first_name"].max_length == 80)

    def test_sign_up_form_last_name_fields(self):
        """User application sign up form last name fields test
        Check SignUpForm last_name field set up is right
        """
        form = SignUpForm()
        self.assertTrue(form.fields["last_name"].__class__.__name__ == "CharField")
        self.assertTrue(form.fields["last_name"].required)
        self.assertTrue(form.fields["last_name"].max_length == 80)

    def test_sign_up_form_email_field(self):
        """Users application sign up form email field test
        Check SignUpForm email field set up is right
        """
        form = SignUpForm()
        self.assertTrue(form.fields["email"].__class__.__name__ == "EmailField")
        self.assertTrue(form.fields["email"].required)

    def test_sign_up_form_password_field(self):
        """Users application sign up form password field test
        Check SignUpForm password field set up is right
        """
        form = SignUpForm()
        self.assertTrue(form.fields["password"].__class__.__name__ == "CharField")
        self.assertTrue(form.fields["password"].required)
        self.assertIsInstance(form.fields["password"].widget, forms.PasswordInput)

    def test_sign_up_form_password_check_field(self):
        """Users application sign up form password_check field test
        Check SignUpForm password_check field set up is right
        """
        form = SignUpForm()
        self.assertTrue(form.fields["password_check"].__class__.__name__ == "CharField")
        self.assertTrue(form.fields["password_check"].required)
        self.assertTrue(form.fields["password_check"].label == "Confirm Password")
        self.assertIsInstance(form.fields["password_check"].widget, forms.PasswordInput)
