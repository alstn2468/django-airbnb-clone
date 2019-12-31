from django.shortcuts import render
from rooms.models import Room


def all_rooms(request):
    rooms = Room.objects.all()

    return render(request, "rooms/home.html", {"rooms": rooms})
