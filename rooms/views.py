from django.shortcuts import render
from django.core.paginator import Paginator
from rooms.models import Room
from math import ceil


def all_rooms(request):
    page = request.GET.get("page", 1)
    room_qs = Room.objects.all()

    paginator = Paginator(room_qs, 10)
    rooms = paginator.get_page(page)

    return render(request, "rooms/home.html", {"rooms": rooms})
