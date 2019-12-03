from django.contrib import admin
from reservations.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Register Reservation model at admin panel"""

    pass
