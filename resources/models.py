from django.db import models

class Resource(models.Model):
    CATEGORY_CHOICES = (
        ('general', 'General'),
        ('stress', 'Stress'),
        ('anxiety', 'Anxiety'),
        ('sleep', 'Sleep'),
        ('depression', 'Depression'),
        ('exam', 'Exam Stress'),
    )

    SEVERITY_CHOICES = (
        ('all', 'All'),
        ('minimal', 'Minimal'),
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20)  # video / audio / guide
    link = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='all')
    usage_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class CommunityLink(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    form_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
