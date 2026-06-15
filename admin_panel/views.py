from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, DeleteView, TemplateView
from django.views import View
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.db.models import Sum

from users.models import User, TrainerProfile
from memberships.models import Branch, Plan, MemberShip

from decimal import Decimal


class LoginAdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.role != "admin":
            raise PermissionDenied("Admins only.")

        return super().dispatch(request, *args, **kwargs)


class AdminDashboardView(LoginAdminRequiredMixin, TemplateView):
    template_name = "admin_panel/admin_dashboard.html"

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


class AdminUserView(LoginAdminRequiredMixin, TemplateView):
    template_name = "admin_panel/admin_user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        members = User.objects.filter(role="member").select_related("user_information")
        admins = User.objects.filter(role="admin").select_related("user_information")

        #-----------stats-------------#
        member_count = members.count()
        admin_count = admins.count()

        context = ({
            "members": members, "admins": admins, 
            "member_count": member_count, "admin_count": admin_count,
        })
        return context


class AdminTrainerView(LoginAdminRequiredMixin, TemplateView):
    template_name = "admin_panel/admin_trainer.html"

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

class AdminBranchPlanView(LoginAdminRequiredMixin, TemplateView):
    template_name = "admin_panel/admin_branch_plan.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        branches = Branch.objects.all()
        plans = Plan.objects.select_related("branch")

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
            "branch_count": branches.count(), "plan_count": plans.count(),
            "branchs_income": branches_income_qs, "branch_salaries": branch_salaries,
        })

        return context

class PromoteMemberView(LoginAdminRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.role = "admin"
        user.save()

        return redirect("admin-user")


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


class BranchCreateView(LoginAdminRequiredMixin, CreateView):
    model = Branch
    fields = ["branch_name", "city"]
    template_name = "admin_panel/admin_panel.html"
    success_url = reverse_lazy("admin-branch-plan")


class BranchDeleteView(LoginAdminRequiredMixin, DeleteView):
    model = Branch
    template_name = "admin_panel/admin_panel.html"
    success_url = reverse_lazy("admin-branch-plan")


class PlanCreateView(LoginAdminRequiredMixin, CreateView):
    model = Plan
    fields = ["branch", "plan_name", "price", 
              "duration", "number_of_sessions", 
              "number_of_spa_sessions", "number_of_suana_sessions", 
              "number_of_jacuzzi_sessions"]
    
    template_name = "admin_panel/admin_panel.html"
    success_url = reverse_lazy("admin-branch-plan")


class PlanDeleteView(LoginAdminRequiredMixin, DeleteView):
    model = Plan
    template_name = "admin_panel/admin_panel.html"
    success_url = reverse_lazy("admin-branch-plan")