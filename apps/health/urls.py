# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('check/', views.health_check, name='health_check'),
]