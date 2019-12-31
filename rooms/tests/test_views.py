from django.test import TestCase
from django.http import HttpRequest
from rooms.views import all_rooms


class RoomViewTest(TestCase):
    def test_rooms_app_all_rooms_view(self):
        """Rooms application all_rooms view test
        Check all_rooms HttpResponse content data contain right title
        """
        request = HttpRequest()
        response = all_rooms(request)

        html = response.content.decode("utf8")
        self.assertIn("<title>All Rooms</title>", html)
