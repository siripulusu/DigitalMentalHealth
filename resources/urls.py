from django.urls import path
from .views import resources_view, community_view

urlpatterns = [
    path('', resources_view, name='resources'),
    path('community/', community_view, name='community'),
]
