from django.test import TestCase
from django.urls import resolve
from users.views import LoginView


class UsersUrlTest(TestCase):
    def test_url_resolves_to_room_deatil(self):
        """Room application '/users/login' pattern urls test
        Check '/users/login' pattern resolved class is RoomDetail
        """
        found = resolve("/users/login")
        self.assertEqual(found.func.view_class, LoginView)
