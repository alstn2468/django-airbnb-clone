from django.test import TestCase
from django.urls import resolve
from rooms.views import room_detail


class RoomsUrlTest(TestCase):
    def test_url_resolves_to_room_deatil(self):
        """Core application '/rooms/1' pattern urls test
        Check '/rooms/1' pattern resolved func is room_detail
        """
        found = resolve("/rooms/1")
        self.assertEqual(found.func, room_detail)

