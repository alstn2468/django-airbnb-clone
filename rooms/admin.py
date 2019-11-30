from django.contrib import admin
from .models import Room, RoomType, Amenity, Facility, HouseRule, Photo


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Register Room model at admin panel"""

    pass


@admin.register(RoomType, Amenity, Facility, HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """Register model classes inherited from the AbstractItem model"""

    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Register Photo model at admin panel"""

    pass
