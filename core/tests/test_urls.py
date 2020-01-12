from django.test import TestCase
from django.urls import resolve
from rooms.views import HomeView


class CoreUrlTest(TestCase):
    def test_root_url_resolves_to_home_view(self):
        """Core application '/' pattern urls test
        Check '/' pattern resolved class is HomeView
        """
        found = resolve("/")
        self.assertEqual(found.func.view_class, HomeView)

