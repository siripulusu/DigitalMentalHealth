from django.urls import path
from .views import resources_view, community_view

urlpatterns = [
    # Dynamic recommended resources (uses assessment severity if logged in)
    path('', resources_view, name='resources'),
    path('recommended/', resources_view, name='recommended_resources'),

    # Peer support / community links
    path('community/', community_view, name='community'),
]
