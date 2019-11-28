from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user("test")

    def test_user_create(self):
        user = User.objects.get(id=1)
        self.assertEqual("test", user.username)
        self.assertEqual("User", user.__class__.__name__)

