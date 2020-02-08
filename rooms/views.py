from django.views.generic import ListView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import Http404
from rooms.models import Room


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


def room_detail(request, pk):
    try:
        room = Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})

    except Room.DoesNotExist:
        raise Http404()

