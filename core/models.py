from django.db import models


class TimeStamp(models.Model):
    """TimeStamp Model

    Inherit:
        Model
    """

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        abstract = True
