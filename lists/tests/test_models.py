from django.test import TestCase
from django.db import IntegrityError
from lists.models import List
from users.models import User
from rooms.models import Room
from datetime import datetime
from unittest import mock
import pytz


class ListModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running ListModelTest

        Fields:
            id         : 1
            name       : Test List 1
            user       : test_user
            rooms      : <Test Room 1, Test Room 2, ... Test Room 10>
            created_at : 2019.11.30.00.00.00
            updated_at : 2019.12.01.00.00.00
        """
        user = User.objects.create_user("test_user")
        mocked = datetime(2019, 11, 30, 0, 0, 0, tzinfo=pytz.utc)

        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            List.objects.create(name="Test List 1", user=user)

    def test_list_create_success(self):
        """List model creation success test
        Check unique field and instance's class name
        """
        list_obj = List.objects.get(id=1)
        self.assertEqual("List", list_obj.__class__.__name__)
        self.assertEqual("test_user", list_obj.user.username)

    def test_list_create_fail(self):
        """List model creation failure test
        List model only can contain null at rooms field, IntegrityError exception
        """
        with self.assertRaises(IntegrityError):
            List.objects.create()

    def test_list_rooms_blank(self):
        """List model rooms field blank test
        Check list's rooms field exists return False
        """
        list_obj = List.objects.get(id=1)
        self.assertFalse(list_obj.rooms.exists())

    def test_list_rooms_set(self):
        """List model rooms field set test
        Check list's rooms field exists return True
        Check list's rooms queryset count equal 10
        Check List model's all query set name equal name format
        """
        user = User.objects.get(id=1)
        list_obj = List.objects.get(id=1)

        for i in range(1, 11):
            room = Room.objects.create(
                name=f"Test Room {i}",
                description=f"Test Description {i}",
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
            list_obj.rooms.add(room)
        self.assertTrue(list_obj.rooms.exists())
        self.assertEqual(list_obj.rooms.count(), 10)

        if list_obj.rooms.exists():
            for idx, room in enumerate(list_obj.rooms.all()):
                self.assertEqual(f"Test Room {idx + 1}", room.name)

    def test_list_str_method(self):
        """List model str method test
        Check str method equal __str__ method return format
        """
        list_obj = List.objects.get(id=1)
        self.assertEqual("Test List 1", str(list_obj))

    def test_list_time_stamp_created_at(self):
        """TimeStamp model created_at test
        Check Test List 1's created_at field is datetime (2019.11.30)
        """
        list_obj = List.objects.get(id=1)
        mocked = datetime(2019, 11, 30, 0, 0, 0, tzinfo=pytz.utc)
        self.assertEqual(list_obj.created_at, mocked)

    def test_list_time_stamp_updated_at(self):
        """TimeStamp model updated_at test
        Get Test List 1 objects and update Test List 1 object
        Check Test List 1's updated_at field is datetime (2019.12.01)
        """
        list_obj = List.objects.get(id=1)
        mocked = datetime(2019, 12, 1, 0, 0, 0, tzinfo=pytz.utc)

        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            list_obj.name = "Update Test List 1"
            list_obj.save()
            self.assertEqual("Update Test List 1", list_obj.name)
            self.assertEqual(list_obj.updated_at, mocked)

    def test_list_count_rooms_method(self):
        """List model count_rooms method test
        Check list model's count_rooms method return value equal room counts
        """
        user = User.objects.get(id=1)
        list_obj = List.objects.get(id=1)

        self.assertEqual(0, list_obj.count_rooms())

        for i in range(1, 11):
            room = Room.objects.create(
                name=f"Test Room {i}",
                description=f"Test Description {i}",
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
            list_obj.rooms.add(room)

        self.assertEqual(10, list_obj.count_rooms())
