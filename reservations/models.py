from django.db import models
from django.utils import timezone
from core.models import AbstractTimeStamp


class Reservation(AbstractTimeStamp):
    """Reservation Model

    Inherit:
        AbstractTimeStamp

    Fields:
        status     : CharField
        check_in   : DateField
        check_out  : DateField
        guest      : User Model (1:N)
        room       : Room Model (1:N)
        created_at : DateTimeField
        updated_at : DateTimeField

    Method:
        __str__     : return room name - check in
        in_progress : return reservation is progress
        is_finished : return reservation is finished
    """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()

        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()

        return now > self.check_out

    is_finished.boolean = True
