from django.db.models import Sum
from django.shortcuts import redirect, get_object_or_404

from django.views.generic import TemplateView
from django.views import View
from .mixins import LoginAdminRequiredMixin

from users.models import User, TrainerProfile


class AdminTrainerView(LoginAdminRequiredMixin, TemplateView):
    template_name = "admins/trainer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        trainers = TrainerProfile.objects.select_related(
            "user", "user__user_information"
        )

        active_trainers = trainers.filter(is_active=True, is_fired=False)
        fired_trainers = trainers.filter(is_fired=True)
        pending_trainers = trainers.filter(is_active=False, is_fired=False)

        trainers_income_qs = TrainerProfile.objects.annotate(
            income=Sum(
                "user__trainer_members__member__member_memberships__amount_paid"
            )
        )

        context.update({
            "trainers": trainers, "active_trainers": active_trainers,
            "fired_trainers": fired_trainers, "pending_trainers": pending_trainers,
            "trainer_count": trainers.count(),  "active_trainer_count": active_trainers.count(),
            "fired_trainer_count": fired_trainers.count(),
            "pending_trainer_count": pending_trainers.count(), 
            "trainers_income": trainers_income_qs,
        })

        return context


class HireTrainerView(LoginAdminRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)

        trainer_profile = user.trainer_profile
        trainer_profile.is_active = True
        trainer_profile.is_fired = False
        trainer_profile.save()

        return redirect("admin-trainer")


class FireTrainerView(LoginAdminRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)

        trainer_profile = user.trainer_profile
        trainer_profile.is_active = False
        trainer_profile.is_fired = True
        trainer_profile.save()

        return redirect("admin-trainer")