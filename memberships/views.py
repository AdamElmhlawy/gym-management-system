from django.views.generic import TemplateView
from .models import Branch, Plan
from users.models import User, TrainerProfile

class HomeListView(TemplateView):
    template_name = "memberships/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = User.objects.filter(role="member").select_related("user_information")
        context["trainers"] = TrainerProfile.objects.select_related("user", "user__user_information")
        context["branches"] = Branch.objects.all()
        context["plans"] = Plan.objects.select_related("branch")
        context["member_count"] = context["members"].count()
        context["trainer_count"] = context["trainers"].count()
        context["branch_count"] = context["branches"].count()
        context["plan_count"] = context["plans"].count()
        context["total_users"] = context["trainer_count"] + context["member_count"]

        return context