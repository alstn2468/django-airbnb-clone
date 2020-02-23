from django.test import TestCase
from rooms.models import RoomType
from rooms.forms import SearchForm


class SearchFormTest(TestCase):
    @classmethod
    def setUpTestData(self):
        """Run only once when running SearchFormTest
        Create 5 RoomType objects for search form test
        """
        for i in range(5):
            RoomType.objects.create(name=f"Room Type {i + 1}")

    def test_search_form_city_field(self):
        """Room application search form city field test
        Check city field set up is right
        """
        form = SearchForm()
        self.assertTrue(form.fields["city"].initial == "Anywhere")

    def test_search_form_country_field(self):
        """Room application search form country field test
        Check country field set up is right
        """
        form = SearchForm()
        self.assertTrue(form.fields["country"].initial == "KR")

    def test_search_form_room_type_field(self):
        """Room application search form room_type field test
        Check room_type field set up is right
        """
        form = SearchForm()
        room_types = RoomType.objects.all()
        self.assertFalse(form.fields["room_type"].required)
        self.assertCountEqual(room_types, form.fields["room_type"].queryset)
        self.assertTrue(form.fields["room_type"].empty_label == "Any Kind")

    def test_search_form_price_field(self):
        """Room application search form price field test
        Check price field set up is right
        """
        form = SearchForm()
        self.assertFalse(form.fields["price"].required)

    def test_search_form_guests_field(self):
        """Room application search form guests field test
        Check guests field set up is right
        """
        form = SearchForm()
        self.assertFalse(form.fields["guests"].required)

    def test_search_form_bedrooms_field(self):
        """Room application search form bedrooms field test
        Check bedrooms field set up is right
        """
        form = SearchForm()
        self.assertFalse(form.fields["bedrooms"].required)

    def test_search_form_beds_field(self):
        """Room application search form beds field test
        Check beds field set up is right
        """
        form = SearchForm()
        self.assertFalse(form.fields["beds"].required)

    def test_search_form_baths_field(self):
        """Room application search form baths field test
        Check baths field set up is right
        """
        form = SearchForm()
        self.assertFalse(form.fields["baths"].required)
