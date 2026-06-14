from django.urls import path
from .views import register

urlpatterns = [
    path('sign-up/', register, name="sign-up"),
]
