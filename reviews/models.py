from django.db import models
from core.models import AbstractTimeStamp


class Review(AbstractTimeStamp):
    """Review model

    Inherit:
        AbstractTimeStamp

    Fields:
        review        : TextField
        accuracy      : IntegerField
        communication : IntegerField
        cleanliness   : IntegerField
        location      : IntegerField
        check_in      : IntegerField
        value         : IntegerField
        user          : User Model (1:N)
        room          : Room Model (1:N)
    """

    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.review} - {self.room}"
