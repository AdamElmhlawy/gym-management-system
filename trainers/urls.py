from django.urls import path
from .views import TrainerProfileCreateView

urlpatterns = [
    path("trainers/<int:user_id>/create", TrainerProfileCreateView.as_view(), name="trainer-profile-create")
]