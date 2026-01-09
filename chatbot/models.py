from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class ChatSession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} ({self.user or 'Anonymous'})"


class ChatMessage(models.Model):
    session = models.ForeignKey(
        ChatSession,
        related_name="messages",
        on_delete=models.CASCADE
    )
    sender = models.CharField(
        max_length=10,
        choices=(("user", "User"), ("bot", "Bot"))
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.message[:30]}"
