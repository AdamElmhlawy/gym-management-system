from django.db.models import Sum

from django.views.generic import TemplateView
from .mixins import LoginAdminRequiredMixin

from users.models import User, TrainerProfile
from members.models import MemberShip



class AdminDashboardView(LoginAdminRequiredMixin, TemplateView):
    template_name = "admins/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)



        #-----------stats-------------#
        member_count = User.objects.filter(role="member").count()
        trainer_count = TrainerProfile.objects.count()

        income_total = (
            MemberShip.objects.aggregate(total=Sum("amount_paid"))["total"] or 0
        )

        total_salaries = (
            TrainerProfile.objects.aggregate(total=Sum("salary"))["total"] or 0
        )

        context = ({
            "total_income": income_total, "total_salaries": total_salaries,
            "total_users": member_count + trainer_count,
        })
        return context