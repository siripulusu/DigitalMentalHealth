from django.urls import path
from .views import phq9_view, gad7_view, assessment_history, download_assessment_pdf

urlpatterns = [
    path('phq9/', phq9_view, name='phq9'),
    path('gad7/', gad7_view, name='gad7'),
    path('history/', assessment_history, name='assessment_history'),
    path('download-pdf/', download_assessment_pdf, name='download_assessment_pdf'),
]
