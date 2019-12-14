from django.db import models
from core.models import AbstractTimeStamp


class Conversation(AbstractTimeStamp):
    """Conversation Model

    Inherit:
        AbstractTimeStamp

    Fields:
        participants : User Model (N:N)
        created_at   : DateTimeField
        updated_at   : DateTimeField
    """

    participants = models.ManyToManyField(
        "users.User", related_name="conversation", blank=True
    )

    def __str__(self):
        usernames = [user.username for user in self.participants.all()]

        return ", ".join(usernames)

    def count_messages(self):
        return self.messages.count()


class Message(AbstractTimeStamp):
    """Message Model

    Inherit:
        AbstractTimeStamp

    Fields:
        message      : TextField
        user         : User Model (1:N)
        conversation : Conversation Model (1:N)
        created_at   : DateTimeField
        updated_at   : DateTimeField
    """

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"
