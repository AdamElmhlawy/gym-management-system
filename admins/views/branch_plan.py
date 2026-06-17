from decimal import Decimal

from django.core.paginator import Paginator
from django.db.models import Sum
from django.urls import reverse_lazy

from django.views.generic import CreateView, DeleteView, TemplateView
from .mixins import LoginAdminRequiredMixin
from members.models import Branch, Plan, MemberShip
from users.models import TrainerProfile



class AdminBranchPlanView(LoginAdminRequiredMixin, TemplateView):
    template_name = "admins/branch_plan.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        branches = Branch.objects.all()
        plans = Plan.objects.select_related("branch")

        # pagination changes for branch_plan
        branch_page_number = self.request.GET.get("branch_page")
        plan_page_number = self.request.GET.get("plan_page")
        branches = Paginator(branches, 10).get_page(branch_page_number)
        plans = Paginator(plans, 10).get_page(plan_page_number)

        branches_income_qs = Branch.objects.annotate(
            income=Sum(
                "user_branch__user__member_memberships__amount_paid"
            )
        )
        branch_salaries = TrainerProfile.objects.aggregate(
            total=Sum("salary")
        )["total"] or Decimal("0.0")

        plan_income = MemberShip.objects.aggregate(
            total=Sum("amount_paid")
        )["total"] or Decimal("0.0")

        context.update({
            "branches": branches, "plans": plans, "plan_income": plan_income,
            "branch_count": branches.paginator.count, "plan_count": plans.paginator.count,
            "branchs_income": branches_income_qs, "branch_salaries": branch_salaries,
        })

        return context

class BranchCreateView(LoginAdminRequiredMixin, CreateView):
    model = Branch
    fields = ["branch_name", "city"]
    template_name = "admins/branch_plan.html"
    success_url = reverse_lazy("admin-branch-plan")


class BranchDeleteView(LoginAdminRequiredMixin, DeleteView):
    model = Branch
    template_name = "admin_panel/branch_plan.html"
    success_url = reverse_lazy("admin-branch-plan")


class PlanCreateView(LoginAdminRequiredMixin, CreateView):
    model = Plan
    fields = ["branch", "plan_name", "price", 
              "duration", "number_of_sessions", 
              "number_of_spa_sessions", "number_of_suana_sessions", 
              "number_of_jacuzzi_sessions"]
    
    template_name = "admins/branch_plan.html.html"
    success_url = reverse_lazy("admin-branch-plan")


class PlanDeleteView(LoginAdminRequiredMixin, DeleteView):
    model = Plan
    template_name = "admins/branch_plan.html"
    success_url = reverse_lazy("admin-branch-plan")