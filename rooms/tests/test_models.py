from django.test import TestCase
from django.db import IntegrityError
from rooms.models import Room


class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running RoomModelTest

        Fields :
            id       : 1
        """
        Room.objects.create()

    def setUp(self):
        """Run every test function

        Fields :
            id           : 2
        """
        Room.objects.create()

    def test_room_create_success(self):
        """Room model creation success test
        Check unique field and instance's class name
        """
        room = Room.objects.get(id=2)
        self.assertEqual("room unique key", "room unique key")
        self.assertEqual("Room", room.__class__.__name__)

    def test_room_create_fail(self):
        """Room model creation failure test
        Duplicate unique key with IntegrityError exception
        """
        with self.assertRaises(IntegrityError):
            Room.objects.create(id=2)
