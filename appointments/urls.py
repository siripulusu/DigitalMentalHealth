from django.urls import path
from .views import book_appointment, counsellor_appointments, add_guidance

urlpatterns = [
    path('book/', book_appointment, name='book_appointment'),
    path('counsellor/', counsellor_appointments, name='counsellor_appointments'),
    path('guidance/<int:appointment_id>/', add_guidance, name='add_guidance'),
]
