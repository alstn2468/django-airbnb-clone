from django.contrib import admin
from conversations.models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Register Conversation model at admin panel"""

    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Register Message model at admin panel"""

    pass
