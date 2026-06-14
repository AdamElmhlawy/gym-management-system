from django.shortcuts import render
from .models import Branch, Plan
from users.models import User, TrainerProfile


def home_view(request):
    members = User.objects.filter(role="member").select_related("user_information")
    trainers = TrainerProfile.objects.select_related("user", "user__user_information")
    branches = Branch.objects.all()
    plans = Plan.objects.select_related("branch")

    context = {
        "members": members,
        "trainers": trainers,
        "branches": branches,
        "plans": plans,
        "member_count": members.count(),
        "trainer_count": trainers.count(),
        "branch_count": branches.count(),
        "plan_count": plans.count(),
        "total_users": members.count() + trainers.count(),
    }

    return render(request, "memberships/home.html", context)

