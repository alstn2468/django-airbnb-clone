from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from rooms.models import Room, RoomType, Amenity, Facility
from django_countries import countries


class HomeView(ListView):
    """rooms application HomeView class
    Display list of room query set

    Inherit             : ListView
    Model               : Room
    paginate_by         : 10
    paginate_orphans    : 5
    ordering            : created_at
    context_object_name : rooms
    Templates name      : rooms/rooms_list.html
    """

    model = Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created_at"
    context_object_name = "rooms"

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(HomeView, self).dispatch(request, *args, **kwargs)

        except Http404:
            return redirect(reverse("core:home"))


class RoomDetail(DetailView):
    """rooms application RoomDetail Class
    Display detail of room object

    Inherit : DetailView
    Model   : Room
    """

    model = Room


def search(request):
    """rooms aplication search method
    Display list of rooms searched by city

    Params
        request : HttpRequest

    Return
        rendered rooms/search.html
    """
    city = request.GET.get("city", "anywhere")
    selected_country = request.GET.get("country", "KR")
    selected_room_type = int(request.GET.get("room-type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = request.GET.get("instant", False)
    is_superhost = request.GET.get("superhost", False)
    checked_amenities = request.GET.getlist("amenities")
    checked_facilities = request.GET.getlist("facilities")

    if city == "":
        city = "anywhere"

    city = str.capitalize(city)

    form = {
        "city": city,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "instant": instant,
        "is_superhost": is_superhost,
        "selected_room_type": selected_room_type,
        "selected_country": selected_country,
        "checked_amenities": checked_amenities,
        "checked_facilities": checked_facilities,
    }

    room_types = RoomType.objects.all()
    amenities = Amenity.objects.all()
    facilities = Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    return render(request, "rooms/search.html", {**form, **choices})
