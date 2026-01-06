from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('counsellor', 'Counsellor'),
        ('peer', 'Peer Volunteer'),
        ('admin', 'Admin'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    anonymous_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"
from django.utils import timezone
from datetime import timedelta

class EmailOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"OTP for {self.user.username}"
