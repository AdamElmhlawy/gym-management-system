from django.urls import path
from .views import (AdminDashboardView, AdminUserView, AdminTrainerView, AdminBranchPlanView,
                    PromoteMemberView, HireTrainerView, FireTrainerView, 
                    BranchCreateView, BranchDeleteView, PlanCreateView, PlanDeleteView)

urlpatterns = [
    path("dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("users/", AdminUserView.as_view(), name="admin-user"),
    path("trainers/", AdminTrainerView.as_view(), name="admin-trainer"),
    path("branched-plans/", AdminBranchPlanView.as_view(), name="admin-branch-plan"),

    path("member/promote/<int:user_id>" , PromoteMemberView.as_view(), name="promote-member"),
    path("trainer/accept/<int:user_id>", HireTrainerView.as_view(), name="accept-trainer"),
    path("trainer/fire/<int:user_id>", FireTrainerView.as_view(), name="fire-trainer"),

    path("branch/create/", BranchCreateView.as_view(), name="create-branch"),
    path("branch/delete/<int:branch_id>", BranchDeleteView.as_view(), name="delete-branch"),
    
    path("plan/create/", PlanCreateView.as_view(), name="create-plan"),
    path("plan/delete/<int:plan_id>", PlanDeleteView.as_view(), name="delete-plan"),
]
