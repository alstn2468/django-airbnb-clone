from django.views.generic import ListView
from django.utils import timezone
from rooms.models import Room

# from django.shortcuts import redirect
# from django.core.paginator import EmptyPage, InvalidPage


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

    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         page = int(request.GET.get("page", 1))
    #         return super(HomeView, self).dispatch(request, *args, **kwargs)

    #     except EmptyPage or ValueError or InvalidPage:
    #         return redirect("/")

    # def render_to_response(self, context):
    #     try:
    #         page = int(self.request.GET.get("page", 1))

    #         return super(HomeView, self).render_to_response(context)

    #     except EmptyPage or ValueError or InvalidPage:
    #         return redirect("/")
