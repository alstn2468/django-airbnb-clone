from django.test import TestCase
from django.db import IntegrityError
from reviews.models import Review
from users.models import User
from rooms.models import Room
from datetime import datetime
from unittest import mock
import pytz


class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running ReviewModelTest

        Fields :
            id            : 1
            review        : Test Review 1
            accuracy      : 1
            communication : 1
            cleanliness   : 2
            location      : 2
            check_in      : 3
            value         : 3
            user          : test_user
            room          : test_room
            created_at    : 2019.11.30.00.00.00
            updated_at    : 2019.12.01.00.00.00
        """
        user = User.objects.create_user("test_user")
        room = Room.objects.create(
            name="Test Room",
            description="Test Description 1",
            country="KR",
            city="Seoul",
            price=100,
            address="Test Address",
            guests=4,
            beds=2,
            bedrooms=1,
            baths=1,
            check_in=datetime(2019, 1, 1, 9, 30),
            check_out=datetime(2019, 1, 2, 10, 30),
            instant_book=True,
            host=user,
        )
        mocked = datetime(2019, 11, 30, 0, 0, 0, tzinfo=pytz.utc)

        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            Review.objects.create(
                review="Test Review 1",
                accuracy=1,
                communication=1,
                cleanliness=2,
                location=2,
                check_in=3,
                value=3,
                user=user,
                room=room,
            )

    def test_review_create_success(self):
        """Review model creation success test
        Check unique field and instance's class name
        """
        review = Review.objects.get(id=1)
        self.assertEqual("Review", review.__class__.__name__)
        self.assertEqual("Test Review 1", review.review)
        self.assertEqual("test_user", review.user.username)
        self.assertEqual("Test Room", review.room.name)

    def test_review_create_fail(self):
        """Review model creation failure test
        Review model's all fields can't contain NULL, IntegrityError exception
        """
        with self.assertRaises(IntegrityError):
            Review.objects.create()

    def test_review_get_fields(self):
        """Review model get fields data test
        Check review's all fields except when testing create success test
        """
        review = Review.objects.get(id=1)
        self.assertEqual(review.accuracy, 1)
        self.assertEqual(review.communication, 1)
        self.assertEqual(review.cleanliness, 2)
        self.assertEqual(review.location, 2)
        self.assertEqual(review.check_in, 3)
        self.assertEqual(review.value, 3)

    def test_review_str_method(self):
        """Review model str method test
        Check str mehtod equal __str__ method return format
        """
        review = Review.objects.get(id=1)
        self.assertEqual("Test Review 1 - Test Room", str(review))

    def test_review_time_stamp_created_at(self):
        """TimeStamp model created_at test
        Check Test Review 1's created_at field is datetime (2019.11.30)
        """
        review = Review.objects.get(id=1)
        mocked = datetime(2019, 11, 30, 0, 0, 0, tzinfo=pytz.utc)
        self.assertEqual(review.created_at, mocked)

    def test_review_time_stamp_updated_at(self):
        """TimeStamp model updated_at test
        Get Test Review 1 objects and update Test Review 1 object
        Check Test Review 1's updated_at field is datetime (2019.12.01)
        """
        review = Review.objects.get(id=1)
        mocked = datetime(2019, 12, 1, 0, 0, 0, tzinfo=pytz.utc)

        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            review.location = 1
            review.save()
            self.assertEqual(review.updated_at, mocked)

    def test_review_rating_average_method(self):
        """Review model rating_average method test
        Check method result equal calculated directly result
        """
        review = Review.objects.get(id=1)
        avg = round(
            (
                review.accuracy
                + review.communication
                + review.cleanliness
                + review.location
                + review.check_in
                + review.value
            )
            / 6,
            2,
        )

        self.assertEqual(avg, review.rating_average())
