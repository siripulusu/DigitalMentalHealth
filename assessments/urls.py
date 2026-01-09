from django.urls import path
from . import views

urlpatterns = [
    path("", views.assessment_home, name="assessments_home"),
    path("phq9/", views.phq9_view, name="phq9"),
    path("gad7/", views.gad7_view, name="gad7"),
    path("history/", views.assessment_history, name="assessment_history"),
    path('download-pdf/', views.download_assessment_pdf, name='download_assessment_pdf'),
]
