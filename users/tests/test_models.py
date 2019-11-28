from django.test import TestCase
from django.db import IntegrityError
from users.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user("test_user_1")

    def test_user_create_success(self):
        user = User.objects.create_user("test_user_2")
        self.assertEqual("test_user_2", user.username)
        self.assertEqual("User", user.__class__.__name__)

    def test_user_create_fail(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user("test_user_1")

