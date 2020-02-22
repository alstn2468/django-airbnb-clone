from django import forms
from rooms.models import RoomType


class SearchForm(forms.Form):
    """Room application search form

    Inherit:
        forms.Form

    Field:
        city  : CharField
        price : IntegerField()
    """

    city = forms.CharField(initial="Anywhere")
    price = forms.IntegerField()
    room_type = forms.ModelChoiceField(queryset=RoomType.objects.all())
