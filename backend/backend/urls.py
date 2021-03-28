"""backend URL Configuration"""
from django.urls import path
from rest_api.views import get_registrations, post_registrations

urlpatterns = [
    path('api/v1/registrations', post_registrations, name='post_registrations_endpoint'),
    path('api/v1/registrations/<str:registrationId>', get_registrations, name='get_registrations_endpoint'),
]
