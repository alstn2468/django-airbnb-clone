from django.contrib import admin
from .models import Room, RoomType, Amenity, Facility, HouseRule


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Register Room model at admin panel"""

    pass


@admin.register(RoomType, Amenity, Facility, HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """Register model classes inherited from the AbstractItem model"""

    pass
