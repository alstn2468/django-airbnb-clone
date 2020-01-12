from django.urls import path
from rooms.views import room_detail

app_name = "rooms"

urlpatterns = [path("<int:pk>", room_detail, name="detail")]
