from .trainers_ops import BaseTrainerView



class AdminFiredTrainerView(BaseTrainerView):
    template_name = "admins/fired_trainer.html"
    def get_queryset(self):
        return super().get_queryset().filter(
            is_fired=True
        ).order_by("years_of_experience")

    def get_context_name(self):
        return "fired_trainers"


class AdminPendingTrainerView(BaseTrainerView):
    template_name = "admins/pending_trainer.html"
    def get_queryset(self):
        return super().get_queryset().filter(
            is_active=False,
            is_fired=False
        ).order_by("user__username")

    def get_context_name(self):
        return "pending_trainers"