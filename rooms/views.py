from django.shortcuts import render
from rooms.models import Room


def all_rooms(request):
    page = int(request.GET.get("page", 1))
    PAGE_SIZE = 10

    LIMIT = PAGE_SIZE * page
    OFFSET = LIMIT - PAGE_SIZE

    rooms = Room.objects.all()[OFFSET:LIMIT]

    return render(request, "rooms/home.html", {"rooms": rooms})
