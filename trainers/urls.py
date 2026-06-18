from django.urls import path
from .views import TrainerDetailView, TrainerUpdateView

urlpatterns = [
    path("<int:user_id>/", TrainerDetailView.as_view(), name="trainer-detail"),
    path("<int:user_id>/edit", TrainerUpdateView.as_view(), name="trainer-update"),
]