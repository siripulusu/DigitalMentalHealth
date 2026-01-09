from django.urls import path
from . import views 

urlpatterns = [
    # Main Dashboards
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('counsellor/', views.counsellor_dashboard, name='counsellor_dashboard'),
    path('volunteer/', views.volunteer_dashboard, name='volunteer_dashboard'),
    
    # System Controls
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_read'),
    path('student/log-mood/', views.log_mood, name='log_mood'),
    
    # Admin Specific Pages
    path('admin/users/', views.admin_user_management, name='admin_user_management'),
    path('admin/users/edit/<int:user_id>/', views.admin_edit_user, name='admin_edit_user'),
    path('admin/analytics/', views.admin_analytics, name='admin_analytics'),
    path('admin/communities/', views.manage_communities, name='manage_communities'),
    path('admin/resources/', views.admin_resource_management, name='admin_resource_management'),
    path('admin/download-pdf/', views.download_admin_pdf, name='admin_pdf'),

    # Counsellor Pages
    path('counsellor/assessments/', views.counsellor_assessments, name='counsellor_assessments'),
    path('counsellor/messages/', views.counsellor_messages, name='counsellor_messages'),
    path('counsellor/resources/', views.manage_resources, name='manage_resources'),
    path('counsellor/ethics/', views.counsellor_ethics, name='counsellor_ethics'),

    # Peer Pages
    path('communities/view/', views.community_view, name='community_view'),
    path('volunteer/conversations/', views.peer_conversations, name='peer_conversations'),
    path('volunteer/communities/', views.peer_communities, name='peer_communities'),
    path('volunteer/guidelines/', views.peer_guidelines, name='peer_guidelines'),
    path('volunteer/escalation/', views.peer_escalation, name='peer_escalation'),
]