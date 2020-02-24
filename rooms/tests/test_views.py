from django.test import TestCase
from rooms.models import Room, RoomType, Amenity, Facility
from users.models import User
from datetime import datetime


class RoomViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running RoomViewTest
        Create 23 rooms for RoomViewTest
        """
        user = User.objects.create_user("test_user")

        for i in range(4):
            RoomType.objects.create(name=f"Room Type {i + 1}")

        for i in range(10):
            Amenity.objects.create(name=f"Amenity {i + 1}")
            Facility.objects.create(name=f"Facility {i + 1}")

        for i in range(1, 24):
            if i == 23:
                user = User.objects.get(id=1)
                user.is_superhost = True
                user.save()

            room_type = RoomType.objects.get(id=1)
            amenity = Amenity.objects.get(id=1)
            facility = Facility.objects.get(id=1)

            room = Room.objects.create(
                name=f"Test Room {i}",
                description="Test Description",
                country="KR",
                city="Seoul",
                price=100,
                address="Test Address",
                guests=6,
                beds=3,
                bedrooms=2,
                baths=2,
                check_in=datetime(2019, 1, 1, 9, 30),
                check_out=datetime(2019, 1, 2, 10, 30),
                instant_book=True,
                host=user,
                room_type=room_type,
            )

            room.amenities.add(amenity)
            room.facilities.add(facility)

            facility = Facility.objects.get(id=2)
            room.facilities.add(facility)

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

    def test_view_rooms_search_default_city(self):
        """Room application search test with empty param
        Check city input default value is Anywhere
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")

        self.assertIn("<title>Search | Airbnb</title>", html)
        self.assertIn('<input type="text" name="city" value="Anywhere"', html)

    def test_view_rooms_search_empty_city(self):
        """Room application search test city is empty str
        Check city input default value is Anywhere
        """
        response = self.client.get("/rooms/search/", {"city": ""})
        html = response.content.decode("utf8")

        self.assertIn("<title>Search | Airbnb</title>", html)
        self.assertIn('<input type="text" name="city" value="Anywhere"', html)

    def test_view_rooms_search_country_options_default(self):
        """Room application search view django_countries option test
        Check country select default option KR is selected
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")

        self.assertIn('<option value="KR" selected>', html)

    def test_view_rooms_search_room_types_default(self):
        """Room application search view room types option test
        Check room_type option default value Any Kind is selected
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")

        self.assertIn('<option value="" selected>Any Kind</option>', html)

    def test_view_rooms_search_form_price_default(self):
        """Room application search view price input test
        Check price field deafult input set up is right
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")

        self.assertIn('<input type="number" name="price" id="id_price">', html)

    def test_view_rooms_search_form_guests_default(self):
        """Room application search view guests input test
        Check guests field deafult input set up is right
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")

        self.assertIn('<input type="number" name="guests" id="id_guests">', html)

    def test_view_rooms_search_form_bedrooms_default(self):
        """Room application search view bedrooms input test
        Check bedrooms field deafult input set up is right
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")

        self.assertIn('<input type="number" name="bedrooms" id="id_bedrooms">', html)

    def test_view_rooms_search_form_beds_default(self):
        """Room application search view beds input test
        Check beds field deafult input set up is right
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")

        self.assertIn('<input type="number" name="beds" id="id_beds">', html)

    def test_view_rooms_search_form_baths_default(self):
        """Room application search view baths input test
        Check baths field deafult input set up is right
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")

        self.assertIn('<input type="number" name="baths" id="id_baths">', html)

    def test_view_rooms_search_form_instant_book_default(self):
        """Room application search view instant_book input test
        Check instant_book field deafult input set up is right
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")

        self.assertIn(
            '<input type="checkbox" name="instant_book" id="id_instant_book">', html
        )

    def test_view_rooms_search_form_is_superhost_default(self):
        """Room application search view is_superhost input test
        Check is_superhost field deafult input set up is right
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")

        self.assertIn(
            '<input type="checkbox" name="is_superhost" id="id_is_superhost">', html
        )

    def test_view_rooms_search_form_amenities_default(self):
        """Room application search view amenities input test
        Check all amenities option created right
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")

        amenities = Amenity.objects.all()

        for idx, a in enumerate(amenities):
            self.assertIn(
                '<input type="checkbox" name="amenities" '
                + f'value="{a.id}" id="id_amenities_{idx}">',
                html,
            )

    def test_view_rooms_search_form_facilities_default(self):
        """Room application search view facilities input test
        Check all facilities option created right
        """
        response = self.client.get("/rooms/search/")
        html = response.content.decode("utf8")

        facilities = Facility.objects.all()

        for idx, f in enumerate(facilities):
            self.assertIn(
                '<input type="checkbox" name="facilities" '
                + f'value="{f.id}" id="id_facilities_{idx}">',
                html,
            )

    def test_view_rooms_search_success(self):
        """Room application search view result test
        Check all rooms rendered at search.html except room 24
        """
        response = self.client.get(
            "/rooms/search/",
            {
                "city": "Seoul",
                "country": "KR",
                "price": 100,
                "guests": 6,
                "beds": 3,
                "bedrooms": 2,
                "baths": 2,
                "instant_book": True,
            },
        )
        html = response.content.decode("utf8")
        rooms = Room.objects.all()

        for room in rooms:
            self.assertIn(f"<h3>{room.name}</h3>", html)

    def test_view_rooms_search_suucess_is_superhost(self):
        """Room application search view result test
        Check is_superhost True rooms rendered at search.html
        """
        response = self.client.get(
            "/rooms/search/",
            {
                "city": "Seoul",
                "country": "KR",
                "price": 100,
                "guests": 6,
                "beds": 3,
                "bedrooms": 2,
                "baths": 2,
                "instant_book": True,
                "is_superhost": True,
            },
        )
        html = response.content.decode("utf8")

        self.assertIn("<h3>Test Room 23</h3>", html)

    def test_view_rooms_search_success_room_type(self):
        """Room application search view result test
        Check all rooms rendered at search.html
        """
        response = self.client.get(
            "/rooms/search/", {"city": "Seoul", "country": "KR", "room_type": 1},
        )
        html = response.content.decode("utf8")
        rooms = Room.objects.all()

        for room in rooms:
            self.assertIn(f"<h3>{room.name}</h3>", html)

    def test_view_rooms_search_success_amenity(self):
        """Room application search view result test
        Check all rooms rendered at search.html
        """
        response = self.client.get(
            "/rooms/search/", {"city": "Seoul", "country": "KR", "amenities": [1]},
        )
        html = response.content.decode("utf8")
        rooms = Room.objects.all()

        for room in rooms:
            self.assertIn(f"<h3>{room.name}</h3>", html)

    def test_view_rooms_search_success_facility(self):
        """Room application search view result test
        Check all rooms rendered at search.html
        """
        response = self.client.get(
            "/rooms/search/", {"city": "Seoul", "country": "KR", "facilities": [1, 2]},
        )
        html = response.content.decode("utf8")
        rooms = Room.objects.all()

        for room in rooms:
            self.assertIn(f"<h3>{room.name}</h3>", html)
