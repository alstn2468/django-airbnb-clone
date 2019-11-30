from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Register Room model at admin panel
    
    inherit:
        ModelAdmin
    """

    pass
