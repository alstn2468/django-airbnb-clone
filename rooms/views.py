from django.shortcuts import render
from rooms.models import Room
from math import ceil


def all_rooms(request):
    page = request.GET.get("page", 1)
    page = int(page or 1)

    PAGE_SIZE = 10

    LIMIT = PAGE_SIZE * page
    OFFSET = LIMIT - PAGE_SIZE

    rooms = Room.objects.all()[OFFSET:LIMIT]
    page_count = ceil(Room.objects.count() / PAGE_SIZE)

    return render(
        request,
        "rooms/home.html",
        {
            "rooms": rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count + 1),
        },
    )
