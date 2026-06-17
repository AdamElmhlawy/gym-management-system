from django.shortcuts import redirect, get_object_or_404

from django.core.paginator import Paginator
from django.views import View
from django.views.generic import TemplateView
from .mixins import LoginAdminRequiredMixin

from users.models import User, TrainerProfile


class BaseTrainerView(LoginAdminRequiredMixin, TemplateView):
    paginate_by = 10

    queryset = TrainerProfile.objects.select_related(
        "user",
        "user__user_information",
    )

    def get_queryset(self):
        return self.queryset

    def get_context_name(self):
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = self.get_queryset()
        page = Paginator(queryset, self.paginate_by).get_page(
            self.request.GET.get("page")
        )

        context[self.get_context_name()] = page
        context[f"{self.get_context_name()}_count"] = queryset.count()

        return context
    

class HireTrainerView(LoginAdminRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)

        trainer_profile = user.trainer_profile
        trainer_profile.is_active = True
        trainer_profile.is_fired = False
        trainer_profile.save()

        return redirect("admin-active-trainer")


class FireTrainerView(LoginAdminRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)

        trainer_profile = user.trainer_profile
        trainer_profile.is_active = False
        trainer_profile.is_fired = True
        trainer_profile.save()

        return redirect("admin-fired-trainer")