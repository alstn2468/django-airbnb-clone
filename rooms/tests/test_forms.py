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
        Check SearchForm's fields are set up correctly
        """
        form = SearchForm()
        self.assertTrue(form.fields["city"].initial == "Anywhere")

    def test_search_form_room_type_field(self):
        """Room application search form room_type field test
        Check RoomType queryset is equal to form's room_type queryset
        """
        form = SearchForm()
        room_types = RoomType.objects.all()
        self.assertCountEqual(room_types, form.fields["room_type"].queryset)
