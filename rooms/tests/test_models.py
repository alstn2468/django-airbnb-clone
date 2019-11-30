from django.test import TestCase
from django.db import IntegrityError
from datetime import datetime
from rooms.models import Room
from users.models import User
from unittest import mock
import pytz


class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running RoomModelTest

        Fields :
            id           : 1
            name         : Test Room 1
            description  : Test Description 1
            country      : 대한민국
            city         : Seoul
            price        : 100
            address      : Test Address
            guest        : 4
            beds         : 2
            bedrooms     : 1
            baths        : 1
            check_in     : 09-30
            check_out    : 10-30
            instant_book : True
            host         : test_user
            created_at   : 2019.11.30.00.00.00
            updated_at    : 2019.12.01.00.00.00
        """
        user = User.objects.create_user("test_user")
        mocked = datetime(2019, 11, 30, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            Room.objects.create(
                name="Test Room 1",
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

    def test_room_create_success(self):
        """Room model creation success test
        Check unique field and instance's class name
        """
        room = Room.objects.get(id=1)
        self.assertEqual("Room", room.__class__.__name__)
        self.assertEqual("Test Room 1", room.name)
        self.assertEqual("test_user", room.host.username)

    def test_room_create_fail(self):
        """Room model creation failure test
        Duplicate pk index with IntegrityError exception
        """
        with self.assertRaises(IntegrityError):
            Room.objects.create(pk=1, name="Test Room 2")

    def test_room_get_fields(self):
        """Room model get fields data test
        Check room's all fields except when testing create success test
        """
        room = Room.objects.get(id=1)
        self.assertEqual("Test Description 1", room.description)
        self.assertEqual("대한민국", room.country.name)
        self.assertEqual("Seoul", room.city)
        self.assertEqual(100, room.price)
        self.assertEqual("Test Address", room.address)
        self.assertEqual(4, room.guests)
        self.assertEqual(2, room.beds)
        self.assertEqual(1, room.bedrooms)
        self.assertEqual(1, room.baths)
        self.assertEqual(datetime(2019, 1, 1, 9, 30).time(), room.check_in)
        self.assertEqual(datetime(2019, 1, 1, 10, 30).time(), room.check_out)
        self.assertTrue(room.instant_book)

    def test_time_stamp_created_at(self):
        """TimeStamp model created_at test
        Check Test Room 1's created_at field is datetime (2019.11.30)
        """
        room = Room.objects.get(id=1)
        mocked = datetime(2019, 11, 30, 0, 0, 0, tzinfo=pytz.utc)
        self.assertEqual(room.created_at, mocked)

    def test_time_stamp_updated_at(self):
        """TimeStamp model updated_at test
        Get Test Room 1 objects and update Test Room 1 object
        Check Test Room 1's updated_at field is datetime (2019.12.01)
        """
        room = Room.objects.get(id=1)
        mocked = datetime(2019, 12, 1, 0, 0, 0, tzinfo=pytz.utc)

        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            room.beds = 2
            room.save()
            self.assertEqual(room.updated_at, mocked)

