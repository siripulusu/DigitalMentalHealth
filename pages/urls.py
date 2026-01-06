from django.urls import path
from .views import home, services, contact

urlpatterns = [
    path('', home, name='home'),
    path('services/', services, name='services'),
    path('contact/', contact, name='contact'),
]
