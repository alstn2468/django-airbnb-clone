from django.contrib import admin
from .models import Room, RoomType


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Register Room model at admin panel
    
    Inherit:
        ModelAdmin
    """

    pass


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    """Register RoomType model at admin panel

    Inherit:
        ModelAdmin
    """

    pass
