from django.urls import path
from .views import admin_dashboard, download_admin_pdf

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),
    path('download-pdf/', download_admin_pdf, name='admin_pdf'),
]
