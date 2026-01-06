from django.db import models
from django.conf import settings

class SelfAssessment(models.Model):
    TEST_CHOICES = (
        ('PHQ9', 'PHQ-9'),
        ('GAD7', 'GAD-7'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    anonymous_id = models.CharField(max_length=36, null=True, blank=True)

    test_type = models.CharField(max_length=10, choices=TEST_CHOICES)
    score = models.IntegerField()
    severity = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_type} - {self.severity}"
