from django.test import TestCase
from django.urls import resolve
from rooms.views import RoomDetail, SearchView


class RoomsUrlTest(TestCase):
    def test_url_resolves_to_room_deatil(self):
        """Room application '/rooms/1' pattern urls test
        Check '/rooms/1' pattern resolved class is RoomDetail
        """
        found = resolve("/rooms/1")
        self.assertEqual(found.func.view_class, RoomDetail)

    def test_url_resolves_to_seacrh(self):
        """Room application '/rooms/search/' pattern urls test
        Check '/rooms/search/' pattern resolved function is search
        """
        found = resolve("/rooms/search/")
        self.assertEqual(found.func.view_class, SearchView)

