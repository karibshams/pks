from django.contrib import admin
from .models import Feedback, ChatMessage

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    ordering = ('-created_at',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user_message', 'timestamp')
    ordering = ('-timestamp',)
