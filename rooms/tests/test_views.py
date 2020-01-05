from django.test import TestCase
from rooms.models import Room
from users.models import User
from datetime import datetime


class RoomViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running RoomViewTest
        Create 23 rooms for RoomViewTest
        """
        user = User.objects.create_user("test_user")

        for i in range(1, 24):
            Room.objects.create(
                name=f"Test Room {i}",
                description="Test Description",
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

    def test_view_rooms_app_all_rooms_default_page(self):
        """Rooms application all_rooms view test without pagination param
        Check all_rooms HttpResponse content data contain right data
        """
        response = self.client.get("/")
        rooms = Room.objects.all()[:10]

        html = response.content.decode("utf8")
        self.assertIn("<title>HOME | Airbnb</title>", html)

        for room in rooms:
            self.assertIn(f"<h1>{room} / ${room.price}</h1>", html)

        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        html = response.content.decode("utf8")

        rooms = Room.objects.all()[:10]
        self.assertIn("<title>HOME | Airbnb</title>", html)

        for room in rooms:
            self.assertIn(f"<h1>{room} / ${room.price}</h1>", html)

    def test_view_rooms_app_all_rooms_next_page(self):
        """Rooms application all_rooms view test with pagination param
        Check all_rooms HttpResponse content data contain right data
        """
        response = self.client.get("/", {"page": 2})
        self.assertEqual(200, response.status_code)
        html = response.content.decode("utf8")

        rooms = Room.objects.all()[10:24]
        self.assertIn("<title>HOME | Airbnb</title>", html)

        for room in rooms:
            self.assertIn(f"<h1>{room} / ${room.price}</h1>", html)

    def test_view_rooms_app_all_rooms_page_is_empty_page(self):
        """Rooms application all_rooms view test page param is empty page
        Check all_rooms HttpResponse is redirect to '/' url
        """

        response = self.client.get("/", {"page": "3"})
        self.assertRedirects(response, "/")
