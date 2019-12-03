from django.db import models
from core.models import AbstractTimeStamp


class List(AbstractTimeStamp):
    """List Model

    Inherit:
        AbstractTimeStamp

    FIelds:
        name  : CharField
        user  : User Model (1:N)
        rooms : Room Model (N:N)
    """

    name = models.CharField(max_length=80)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    rooms = models.ManyToManyField("rooms.Room", blank=True)

    def __str__(self):
        return self.name
