from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from rooms.models import Room


def all_rooms(request):
    page = request.GET.get("page", 1)
    room_qs = Room.objects.all()

    paginator = Paginator(room_qs, 10, orphans=5)

    try:
        rooms = paginator.page(int(page))

        return render(request, "rooms/home.html", {"page": rooms})

    except EmptyPage:
        return redirect("/")
