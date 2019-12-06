from django.contrib import admin
from .models import Room, RoomType, Amenity, Facility, HouseRule, Photo


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Register Room model at admin panel

    Filter by:
        instant_book      : BooleanField
        host.is_superhost : BooleanField
        city              : CharField
        room_type         : RoomType Model
        amenities         : Amenity Model
        facilities        : Facility Model
        house_rules       : HouseRule Model
        country           : CharField

    Search by:
        city              : exact
        host.username     : startwith
    """

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "More About the Space",
            {"fields": ("amenities", "facilities", "house_rules")},
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
    )
    list_filter = (
        "instant_book",
        "host__is_superhost",
        "city",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "country",
    )
    filter_horizontal = ("amenities", "facilities", "house_rules")
    search_fields = ("=city", "^host__username")


@admin.register(RoomType, Amenity, Facility, HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """Register model classes inherited from the AbstractItem model"""

    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Register Photo model at admin panel"""

    pass
