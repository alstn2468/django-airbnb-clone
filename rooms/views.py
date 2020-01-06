from django.shortcuts import redirect
from django.views.generic import ListView
from django.core.paginator import EmptyPage, InvalidPage
from rooms.models import Room


class HomeView(ListView):
    """rooms application HomeView class
    Display list of room query set

    Inherit          : ListView
    Model            : Room
    paginate_by      : 10
    paginate_orphans : 5
    ordering         : created_at
    Templates name   : rooms/rooms_list.html
    """

    model = Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created_at"
