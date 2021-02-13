from django.urls import path
from rooms.views import RoomDetailView, SearchView, RoomEditView

app_name = "rooms"

urlpatterns = [
    path("<int:pk>", RoomDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", RoomEditView.as_view(), name="edit"),
    path("search/", SearchView.as_view(), name="search"),
]
