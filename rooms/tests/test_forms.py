from django.test import TestCase
from django import forms
from rooms.models import RoomType, Amenity, Facility
from rooms.forms import SearchForm


class SearchFormTest(TestCase):
    @classmethod
    def setUpTestData(self):
        """Run only once when running SearchFormTest
        Create 5 RoomType objects for search form test
        Create 5 Amenity objects for search form test
        Create 5 Facility objects for search form test
        """
        for i in range(5):
            RoomType.objects.create(name=f"Room Type {i + 1}")
            Amenity.objects.create(name=f"Amenity {i + 1}")
            Facility.objects.create(name=f"Facility {i + 1}")

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

    def test_search_form_instant_book_field(self):
        """Room application search form instant_book field test
        Check instant_book field set up is right
        """
        form = SearchForm()
        self.assertFalse(form.fields["instant_book"].required)

    def test_search_form_is_superhost_field(self):
        """Room application search form is_superhost field test
        Check is_superhost field set up is right
        """
        form = SearchForm()
        self.assertFalse(form.fields["is_superhost"].required)

    def test_search_form_amenities_field(self):
        """Room application search form amenities field test
        Check amenities field set up is right
        """
        form = SearchForm()
        amenities = Amenity.objects.all()
        self.assertCountEqual(amenities, form.fields["amenities"].queryset)
        self.assertIsInstance(
            form.fields["amenities"].widget, forms.CheckboxSelectMultiple
        )
        self.assertFalse(form.fields["amenities"].required)

    def test_search_form_facilities_field(self):
        """Room application search form facilities field test
        Check facilities field set up is right
        """
        form = SearchForm()
        facilities = Facility.objects.all()
        self.assertCountEqual(facilities, form.fields["facilities"].queryset)
        self.assertIsInstance(
            form.fields["facilities"].widget, forms.CheckboxSelectMultiple
        )
        self.assertFalse(form.fields["facilities"].required)
