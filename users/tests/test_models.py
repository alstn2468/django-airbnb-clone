from django.test import TestCase
from django.db import IntegrityError
from django.utils.timezone import now
from users.models import User
import tempfile


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running UserModelTest
        Only set username field

        Fields :
            id       : 1
            username : test_user_1
        """
        User.objects.create_user("test_user_1")

    def setUp(self):
        """Run every test function
        Setting all fields except avatar field

        Fields :
            id              : 2
            username        : test_user_2
            bio             : test_bio
            birth_date      : now date
            language        : en
            currency        : usd
            is_superhost    : True
            email_verified : True
            email_secret    : test
        """
        User.objects.create_user(
            username="test_user_2",
            gender=User.GENDER_MALE,
            bio="test bio",
            birth_date=now().date(),
            language=User.LANGUAGE_ENGLISH,
            currency=User.CURRENCY_USD,
            is_superhost=True,
            email_verified=True,
            email_secret="test",
        )

    def test_user_create_success(self):
        """User model creation success test
        Check username field and instance's class name
        """
        user = User.objects.get(username="test_user_2")
        self.assertEqual("test_user_2", user.username)
        self.assertEqual("User", user.__class__.__name__)

    def test_user_create_fail(self):
        """User model creation failure test
        Duplicate username with IntegrityError exception
        """
        with self.assertRaises(IntegrityError):
            User.objects.create_user("test_user_1")

    def test_user_bio_default(self):
        """User model bio field default value test
        Check test_user_1's bio is ""
        """
        user = User.objects.get(username="test_user_1")
        self.assertEqual("", user.bio)

    def test_user_bio_set(self):
        """User model bio field set value test
        Check test_user_2's bio is "test bio"
        """
        user = User.objects.get(username="test_user_2")
        self.assertEqual("test bio", user.bio)

    def test_user_avatar_blank(self):
        """User model avatar field blank test
        Check test_user_1's bool(avatar) is False
        """
        user = User.objects.get(username="test_user_1")
        self.assertFalse(bool(user.avatar))

    def test_user_avatar_set(self):
        """User model avatar field set file test
        Check test_user_2's avatar equal test_image_file
        test_image_file is a temporary file with the jpg extension
        """
        user = User.objects.get(username="test_user_2")

        test_image_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
        user.avatar = test_image_file
        user.save()

        self.assertEqual(user.avatar, test_image_file)

    def test_user_gender_blank(self):
        """User model gender field blank test
        Check test_user_1's gender is ""
        """
        user = User.objects.get(username="test_user_1")
        self.assertEqual("", user.gender)

    def test_user_gender_set(self):
        """User model gender field set value test
        Check test_user_2's gender equal "male"
        """
        user = User.objects.get(username="test_user_2")
        self.assertEqual("male", user.gender)

    def test_user_birth_date_blank(self):
        """User model birth_date field blank test
        Check test_user_1's birth_date is None
        """
        user = User.objects.get(username="test_user_1")
        self.assertIsNone(user.birth_date)

    def test_user_birth_date_set(self):
        """User model birth_date field set value test
        Check test_user_2's birth_date equal now date
        DateField contains only year, month and day data
        """
        user = User.objects.get(username="test_user_2")
        self.assertEqual(user.birth_date, now().date())

    def test_user_language_default(self):
        """User model language field default test
        Check test_user_1's language is LANGUAGE_KOREAN
        """
        user = User.objects.get(username="test_user_1")
        self.assertEqual(User.LANGUAGE_KOREAN, user.language)

    def test_user_language_set(self):
        """User model language field set value test
        Check test_user_2's language equal "en"
        """
        user = User.objects.get(username="test_user_2")
        self.assertEqual("en", user.language)

    def test_user_currency_default(self):
        """User model currency field default test
        Check test_user_1's currency is CURRENCY_KRW
        """
        user = User.objects.get(username="test_user_1")
        self.assertEqual(User.CURRENCY_KRW, user.currency)

    def test_user_currency_set(self):
        """User model currency field set value test
        Check test_user_2's currency equal "usd"
        """
        user = User.objects.get(username="test_user_2")
        self.assertEqual("usd", user.currency)

    def test_user_is_superhost_default(self):
        """User model is_superhost field default value test
        Check test_user_1's is_superhost is False
        """
        user = User.objects.get(username="test_user_1")
        self.assertFalse(user.is_superhost)

    def test_user_is_superhost_set(self):
        """User model is_superhost field set value test
        Check test_user_2's is_superhost is True
        """
        user = User.objects.get(username="test_user_2")
        self.assertTrue(user.is_superhost)

    def test_user_email_verified_default(self):
        """User model email_verified field default value test
        Check test_user_1's email_verified is False
        """
        user = User.objects.get(username="test_user_1")
        self.assertFalse(user.email_verified)

    def test_user_email_verified_set(self):
        """User model email_verified field set value test
        Check test_user_2's email_verified is True
        """
        user = User.objects.get(username="test_user_2")
        self.assertTrue(user.email_verified)

    def test_user_email_secret_default(self):
        """User model email_secret field default value test
        Check test_user_1's email_secret is empty string
        """
        user = User.objects.get(username="test_user_1")
        self.assertEqual("", user.email_secret)

    def test_user_email_secret_set(self):
        """User model email_secret field set value test
        Check test_user_2's email_secret is "test"
        """
        user = User.objects.get(username="test_user_2")
        self.assertEqual("test", user.email_secret)

    def test_user_verify_email_return_true(self):
        """User model verify_email method test
        Now verify_email return True when unverified user call ths method
        """
        user = User.objects.get(username="test_user_1")
        self.assertTrue(user.verify_email())

    def test_user_verify_email_return_false(self):
        """User model verify_email method test
        Now verify_email return False when verified user call this method
        """
        user = User.objects.get(username="test_user_2")
        self.assertFalse(user.verify_email())
