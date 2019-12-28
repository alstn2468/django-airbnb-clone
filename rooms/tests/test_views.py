from django.test import TestCase
from django.http import HttpRequest
from rooms.views import all_rooms


class RoomViewTest(TestCase):
    def test_rooms_app_all_rooms_view(self):
        """Rooms application all_rooms view test
        Check all_rooms return value is None
        """
        request = HttpRequest()
        response = all_rooms(request)
        self.assertIsNone(response)

