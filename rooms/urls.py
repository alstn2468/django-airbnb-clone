from django.urls import path
from rooms.views import RoomDetail

app_name = "rooms"

urlpatterns = [path("<int:pk>", RoomDetail.as_view(), name="detail")]
