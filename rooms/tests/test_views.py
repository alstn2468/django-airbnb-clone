from django.test import TestCase
from rooms.models import Room, RoomType, Amenity, Facility
from users.models import User
from datetime import datetime
from django_countries import countries


class RoomViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running RoomViewTest
        Create 23 rooms for RoomViewTest
        """
        user = User.objects.create_user("test_user")

        for i in range(1, 24):
            if i == 23:
                user = User.objects.get(id=1)
                user.is_superhost = True
                user.save()

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

        for i in range(4):
            RoomType.objects.create(name=f"Room Type {i + 1}")

        for i in range(10):
            Amenity.objects.create(name=f"Amenity {i + 1}")
            Facility.objects.create(name=f"Facility {i + 1}")

    def test_view_rooms_home_view_default_page(self):
        """Rooms application HomeView test without pagination param
        Check HomeView HttpResponse content data contain right data
        """
        response = self.client.get("/")
        html = response.content.decode("utf8")
        self.assertEqual(200, response.status_code)

        rooms = Room.objects.all().order_by("created_at")[:10]

        self.assertIn("<title>HOME | Airbnb</title>", html)
        self.assertIn('<a href="?page=2">Next</a>', html)

        for room in rooms:
            self.assertIn(f"<a href='/rooms/{room.id}'>", html)
            self.assertIn(f"<h4>{room} / ${room.price}</h4>", html)

    def test_view_rooms_home_view_next_page(self):
        """Rooms application HomeView view test with pagination param
        Check HomeView HttpResponse content data contain right data
        """
        response = self.client.get("/", {"page": 2})
        html = response.content.decode("utf8")
        self.assertEqual(200, response.status_code)

        rooms = Room.objects.all().order_by("created_at")[10:24]

        self.assertIn("<title>HOME | Airbnb</title>", html)
        self.assertIn('<a href="?page=1">Previous</a>', html)

        for room in rooms:
            self.assertIn(f"<a href='/rooms/{room.id}'>", html)
            self.assertIn(f"<h4>{room} / ${room.price}</h4>", html)

    def test_view_rooms_home_view_invalid_page(self):
        """Rooms application HomeView test page param is invalid page
        Check HomeView HttpResponse is redirect to '/' url
        """
        response = self.client.get("/", {"page": "3"})
        self.assertRedirects(response, "/")

    def test_view_rooms_home_view_str_page_param(self):
        """Rooms application HomeView test page param is invalid string
        Check HomeView HttpResponse is redirect to '/' url
        """
        response = self.client.get("/", {"page": "invalid_param"})
        self.assertRedirects(response, "/")

    def test_view_rooms_app_room_detail_success(self):
        """Rooms application RoomDetail test is success
        Check room_deatil HttpResponse contain right room instance data
        """
        response = self.client.get("/rooms/1")
        html = response.content.decode("utf8")
        room = Room.objects.get(pk=1)

        self.assertIn(f"<title>{room.name} | Airbnb</title>", html)
        self.assertIn(room.name, html)
        self.assertIn(room.description, html)
        self.assertIn(f"By : {room.host.username}", html)

    def test_view_rooms_app_room_detail_is_superhost(self):
        """Rooms application RoomDetail test is success and host is superhost
        Check room_deatil HttpResponse contain right room instance data
        """
        response = self.client.get("/rooms/23")
        html = response.content.decode("utf8")
        room = Room.objects.get(pk=23)

        self.assertIn(f"<title>{room.name} | Airbnb</title>", html)
        self.assertIn(room.name, html)
        self.assertIn(room.description, html)
        self.assertIn(f"By : {room.host.username}", html)
        self.assertIn("(superhost)", html)

    def test_view_rooms_app_room_detail_fail(self):
        """Rooms application RoomDetail test catch exception
        Check room_deatil catch DoesNotExist exception then raise Http404
        """
        response = self.client.get("/rooms/25")
        self.assertEqual(404, response.status_code)

    def test_view_rooms_search_success(self):
        """Room application search test is success
        Check search HttpResponse contain right search result
        """
        city = "seoul"
        response = self.client.get("/rooms/search/", {"city": city})
        html = response.content.decode("utf8")

        self.assertIn("<title>Search | Airbnb</title>", html)
        self.assertIn('<input value="Seoul"', html)

    def test_view_rooms_search_default_city(self):
        """Room application search test with empty param
        Check search param city is Anywhere
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")

        self.assertIn("<title>Search | Airbnb</title>", html)
        self.assertIn('<input value="Anywhere"', html)

    def test_view_rooms_search_empty_city(self):
        """Room application search test city is empty str
        Check search param city is Anywhere
        """
        response = self.client.get("/rooms/search/", {"city": ""})
        html = response.content.decode("utf8")

        self.assertIn("<title>Search | Airbnb</title>", html)
        self.assertIn('<input value="Anywhere"', html)

    def test_view_rooms_search_country_options_default(self):
        """Room application search view django_countries option test
        Check contain all countries option in select tag
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")

        self.assertIn('<option value="KR" selected>', html)

        for country in countries:
            self.assertIn(f'<option value="{country.code}"', html)

    def test_view_rooms_search_room_types_default(self):
        """Room application search view room types option test
        Check contain all room tpyes option in select tag
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")
        room_types = RoomType.objects.all()

        self.assertIn('<option value="0" selected>', html)

        for room_type in room_types:
            self.assertIn(f'<option value="{room_type.pk}"', html)

    def test_view_rooms_search_country_options_set(self):
        """Room application search view country option test
        Check country param "AF" option is selected
        """
        response = self.client.get("/rooms/search/", {"country": "AF"})
        html = response.content.decode("utf8")

        self.assertIn('<option value="AF" selected>', html)

    def test_view_rooms_search_room_types_options_set(self):
        """Room application search view room types option test
        Check room-type param "2" option is selected
        """
        response = self.client.get("/rooms/search/", {"room-type": 2})
        html = response.content.decode("utf8")

        self.assertIn('<option value="2" selected>', html)

    def test_view_rooms_search_num_param_default(self):
        """Room application search view number params test
        Check all number params default value is 0
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")

        self.assertIn(
            '<input value="0" type="number" name="price" id="price" placeholder="Price"/>',
            html,
        )
        self.assertIn(
            '<input value="0" type="number" name="guests" id="guests" placeholder="Guests"/>',
            html,
        )
        self.assertIn(
            '<input value="0" type="number" name="bedrooms" id="bedrooms" placeholder="Bedrooms"/>',
            html,
        )
        self.assertIn(
            '<input value="0" type="number" name="beds" id="beds" placeholder="Beds"/>',
            html,
        )
        self.assertIn(
            '<input value="0" type="number" name="baths" id="baths" placeholder="Baths"/>',
            html,
        )

    def test_view_rooms_search_num_param_set(self):
        """Room application search view number params test
        Check all number params default value is set value
        """
        response = self.client.get(
            "/rooms/search/",
            {"price": 10, "guests": 5, "bedrooms": 2, "beds": 1, "baths": 1},
        )
        html = response.content.decode("utf8")

        self.assertIn(
            '<input value="10" type="number" name="price" id="price" placeholder="Price"/>',
            html,
        )
        self.assertIn(
            '<input value="5" type="number" name="guests" id="guests" placeholder="Guests"/>',
            html,
        )
        self.assertIn(
            '<input value="2" type="number" name="bedrooms" id="bedrooms" placeholder="Bedrooms"/>',
            html,
        )
        self.assertIn(
            '<input value="1" type="number" name="beds" id="beds" placeholder="Beds"/>',
            html,
        )
        self.assertIn(
            '<input value="1" type="number" name="baths" id="baths" placeholder="Baths"/>',
            html,
        )

    def test_view_rooms_search_amenities_default(self):
        """Room application search view amenities checkbox test
        Check amenities check box is unchecked
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")
        amenities = Amenity.objects.all()

        for amenity in amenities:
            self.assertIn(
                f'<input id="amenity_{amenity.pk}" type="checkbox" name="amenities" value="{amenity.pk}"/>',
                html,
            )

    def test_view_rooms_search_facilities_default(self):
        """Room application search view facilities checkbox test
        Check facilities check box is unchecked
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")
        facilities = Facility.objects.all()

        for facility in facilities:
            self.assertIn(
                f'<input id="facility_{facility.pk}" type="checkbox" name="facilities" value="{facility.pk}"/>',
                html,
            )