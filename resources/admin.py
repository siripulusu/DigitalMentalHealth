from django.contrib import admin
from .models import Resource, CommunityLink

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'severity', 'resource_type', 'usage_count')
    list_filter = ('category', 'severity', 'resource_type')
    search_fields = ('title',)

@admin.register(CommunityLink)
class CommunityLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
