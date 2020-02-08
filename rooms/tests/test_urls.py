from django.test import TestCase
from django.urls import resolve
from rooms.views import RoomDetail


class RoomsUrlTest(TestCase):
    def test_url_resolves_to_room_deatil(self):
        """Core application '/rooms/1' pattern urls test
        Check '/rooms/1' pattern resolved class is RoomDetail
        """
        found = resolve("/rooms/1")
        self.assertEqual(found.func.view_class, RoomDetail)

