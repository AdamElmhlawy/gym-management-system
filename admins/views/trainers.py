from django.db.models import Sum
from .trainers_ops import BaseTrainerView


class AdminActiveTrainerView(BaseTrainerView):
    template_name = "admins/active_trainer.html"
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).annotate(
        income=Sum("user__trainer_members__member__member_memberships__amount_paid")
    )

    def get_context_name(self):
        return "active_trainer"


