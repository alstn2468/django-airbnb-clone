from django.contrib import admin
from lists.models import List


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    """Register List model at admin panel

    Search by:
        name : icontains
    """

    list_display = ("name", "user", "count_rooms")
    search_fields = ("name",)
