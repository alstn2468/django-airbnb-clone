from django.urls import path
from rooms import views as room_views


app_name = "core"

urlpatterns = [path("", room_views.all_rooms, name="home")]
