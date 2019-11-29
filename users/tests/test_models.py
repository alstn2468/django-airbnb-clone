from django.test import TestCase
from django.db import IntegrityError, models
from users.models import User
import tempfile


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user("test_user_1")

    def setUp(self):
        User.objects.create_user(
            username="test_user_2", bio="test bio", gender=User.GENDER_MALE,
        )

    def test_user_create_success(self):
        user = User.objects.get(username="test_user_2")
        self.assertEqual("test_user_2", user.username)
        self.assertEqual("User", user.__class__.__name__)

    def test_user_create_fail(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user("test_user_1")

    def test_user_bio_default(self):
        user = User.objects.get(username="test_user_1")
        self.assertEqual("", user.bio)

    def test_user_bio_set(self):
        user = User.objects.get(username="test_user_2")
        self.assertEqual("test bio", user.bio)

    def test_user_avatar_blank(self):
        user = User.objects.get(username="test_user_1")
        self.assertFalse(bool(user.avatar))

    def test_user_avatar_set(self):
        user = User.objects.get(username="test_user_2")

        test_image_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
        user.avatar = test_image_file
        user.save()

        self.assertEqual(user.avatar, test_image_file)

    def test_user_gender_blank(self):
        user = User.objects.get(username="test_user_1")
        self.assertIsNone(user.gender)

    def test_user_gender_set(self):
        user = User.objects.get(username="test_user_2")
        self.assertEqual("male", user.gender)

