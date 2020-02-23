from django import forms
from rooms.models import RoomType
from django_countries.fields import CountryField


class SearchForm(forms.Form):
    """Room application search form

    Inherit:
        forms.Form

    Field:
        city      : CharField
        country   : CountryField.formfield
        room_type : ModelChoiceField (RoomType)
        price     : IntegerField
        guests    : IntegerField
        bedrooms  : IntegerField
        beds      : IntegerField
        baths     : IntegerField
    """

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any Kind", queryset=RoomType.objects.all()
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
