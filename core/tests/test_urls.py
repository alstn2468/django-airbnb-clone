from django.test import TestCase
from django.urls import resolve
from rooms.views import all_rooms


class CoreUrlTest(TestCase):
    def test_root_url_resolves_to_all_rooms(self):
        """Core application '/' pattern urls test
        Check '/' pattern resolved func is all_rooms
        """
        found = resolve("/")
        self.assertTrue(found.func, all_rooms)

