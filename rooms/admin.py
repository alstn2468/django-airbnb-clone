from django.contrib import admin
from django.utils.html import mark_safe
from .models import Room, RoomType, Amenity, Facility, HouseRule, Photo


@admin.register(RoomType, Amenity, Facility, HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """Register model classes inherited from the AbstractItem model"""

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Register Photo model at admin panel"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"


class PhotoInlineAdmin(admin.TabularInline):
    """Photo model's inline admin"""

    model = Photo


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

    inlines = (PhotoInlineAdmin,)

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

    raw_id_fields = ("host",)

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
        "count_photos",
        "total_rating",
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

    def count_photos(self, obj):
        return obj.photos.count()
