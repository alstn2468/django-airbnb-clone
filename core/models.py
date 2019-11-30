from django.db import models


class TimeStamp(models.Model):
    """Abstract TimeStamp Model

    Inherit:
        Model

    Fields:
        created_at : DateTImeField (UnEditable)
        updated_at : DateTimeField (Editable)
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
