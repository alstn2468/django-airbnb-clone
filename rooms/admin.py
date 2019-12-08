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

    Admin function :
        count_amenities   : return amenities count
        count_facilities  : return facilities count
        count_house_rules : return house_rules count
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
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules"),
            },
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
        "count_amenities",
        "count_facilities",
        "count_house_rules",
        "count_photos",
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

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_facilities(self, obj):
        return obj.facilities.count()

    def count_house_rules(self, obj):
        return obj.house_rules.count()

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(RoomType, Amenity, Facility, HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """Register model classes inherited from the AbstractItem model"""

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Register Photo model at admin panel"""

    pass
