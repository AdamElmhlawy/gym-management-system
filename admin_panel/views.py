from functools import wraps
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.db.models import Sum

from users.models import User, TrainerProfile
from memberships.models import Branch, Plan, MemberShip


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role != "admin":
            raise PermissionDenied("Only admins can access this endpoint.")
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def admin_panel(request):
    members = User.objects.filter(role="member").select_related("user_information")

    trainers = TrainerProfile.objects.select_related(
        "user", "user__user_information"
    )

    active_trainers = trainers.filter(is_active=True, is_fired=False)
    fired_trainers = trainers.filter(is_fired=True)
    pending_trainers = trainers.filter(is_active=False, is_fired=False)

    admins = User.objects.filter(role="admin").select_related("user_information")
    branches = Branch.objects.all()
    plans = Plan.objects.select_related("branch")

    total_income = MemberShip.objects.aggregate(
        total=Sum("amount_paid")
    )["total"] or 0

    total_salaries = TrainerProfile.objects.aggregate(
        total=Sum("salary")
    )["total"] or 0

    context = {
        "members": members,
        "trainers": trainers,
        "active_trainers": active_trainers,
        "fired_trainers": fired_trainers,
        "pending_trainers": pending_trainers,
        "admins": admins,
        "branches": branches,
        "plans": plans,

        "member_count": members.count(),
        "trainer_count": trainers.count(),
        "active_trainer_count": active_trainers.count(),
        "fired_trainer_count": fired_trainers.count(),
        "pending_trainer_count": pending_trainers.count(),
        "admin_count": admins.count(),
        "branch_count": branches.count(),
        "plan_count": plans.count(),

        "total_users": members.count() + trainers.count(),
        "total_income": total_income,
        "total_salaries": total_salaries,
    }

    return render(request, "admin_panel/admin_panel.html", context)


@login_required
@admin_required
def promote_member(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, pk=user_id)
        user.role = "admin"
        user.save()
    return redirect("admin-panel")


@login_required
@admin_required
def accept_trainer(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, pk=user_id)
        profile = user.trainer_profile
        profile.is_active = True
        profile.is_fired = False
        profile.save()
    return redirect("admin-panel")


@login_required
@admin_required
def fire_trainer(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, pk=user_id)
        profile = user.trainer_profile
        profile.is_active = False
        profile.is_fired = True
        profile.save()
    return redirect("admin-panel")


@login_required
@admin_required
def create_branch(request):
    if request.method == "POST":
        branch_name = request.POST["branch_name"]

        if Branch.objects.filter(branch_name=branch_name).exists():
            return HttpResponse("Branch exists already", status=400)

        valid_cities = [
            "tanta", "cairo", "alexandria", "mansura", "suez",
            "north_sinai", "boston", "london", "berlin",
            "barcelona", "moscow", "stockholm",
        ]

        city = request.POST["city"]

        if city not in valid_cities:
            return HttpResponse("Invalid city", status=400)

        Branch.objects.create(
            branch_name=branch_name,
            city=city
        )

    return redirect("admin-panel")


@login_required
@admin_required
def delete_branch(request, branch_id):
    if request.method == "POST":
        branch = get_object_or_404(Branch, pk=branch_id)
        branch.delete()
    return redirect("admin-panel")


@login_required
@admin_required
def create_plan(request):
    if request.method == "POST":
        branch_id = request.POST.get("branch")

        if not branch_id:
            return HttpResponse("Missing branch", status=400)

        branch = get_object_or_404(Branch, pk=branch_id)

        plan_name = request.POST.get("plan_name", "").strip()

        if Plan.objects.filter(plan_name=plan_name).exists():
            return HttpResponse("Plan already exists", status=400)

        try:
            price = Decimal(request.POST.get("price"))
        except (TypeError, ValueError):
            return HttpResponse("Invalid price", status=400)

        if price < 500:
            return HttpResponse("Price is too low", status=400)

        valid_durations = ["one_month", "three_months", "six_months", "twelve_months"]
        duration = request.POST.get("duration")

        if duration not in valid_durations:
            return HttpResponse("Invalid duration", status=400)

        try:
            sessions = int(request.POST.get("number_of_sessions") or 0)
        except ValueError:
            return HttpResponse("Invalid sessions", status=400)

        Plan.objects.create(
            branch=branch,
            plan_name=plan_name,
            price=price,
            duration=duration,
            number_of_sessions=sessions,
            number_of_spa_sessions=int(request.POST.get("number_of_spa_sessions") or 0),
            number_of_suana_sessions=int(request.POST.get("number_of_suana_sessions") or 0),
            number_of_jacuzzi_sessions=int(request.POST.get("number_of_jacuzzi_sessions") or 0),
        )

    return redirect("admin-panel")


@login_required
@admin_required
def delete_plan(request, plan_id):
    if request.method == "POST":
        plan = get_object_or_404(Plan, pk=plan_id)
        plan.delete()
    return redirect("admin-panel")

@login_required
@admin_required
def promote_member(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, pk=user_id)
        user.role = "admin"
        user.save()
    return redirect("admin-panel")

@login_required
@admin_required
def accept_trainer(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, pk=user_id)
        user.trainer_profile.is_active = True
        user.trainer_profile.is_fired = False
        user.trainer_profile.save()
    return redirect("admin-panel")

@login_required
@admin_required
def fire_trainer(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, pk=user_id)
        user.trainer_profile.is_active = False
        user.trainer_profile.is_fired = True
        user.trainer_profile.save()
    return redirect("admin-panel")

@login_required
@admin_required
def create_branch(request):
    if request.method == "POST":
        branch_name = request.POST["branch_name"]
        if Branch.objects.filter(branch_name=branch_name).exists():
            return HttpResponse("Branch exits already", status=400)
        
        valid_cities = ["tanta", "cairo", "alexandria",
                       "mansura", "suez", "north_sinai",
                       "boston", "london", "berlin",
                       "barcelona", "moscow", "stockholm",]

        city = request.POST["city"]

        if city not in valid_cities:
            return HttpResponse("Invalid city", status=400)

        Branch.objects.create(
            branch_name=branch_name,
            city=city
        )

    return redirect("admin-panel")

@login_required
@admin_required
def delete_branch(request, branch_id):
    if request.method == "POST":
        branch = get_object_or_404(Branch, pk=branch_id)
        branch.delete()

    return redirect("admin-panel")

@login_required
@admin_required
def create_plan(request):
    if request.method == "POST":

        branch_id = request.POST.get("branch")
        if not branch_id:
            return HttpResponse("Missing branch", status=400)

        branch = get_object_or_404(Branch, pk=branch_id)

        plan_name = request.POST.get("plan_name", "").strip()

        if Plan.objects.filter(plan_name=plan_name).exists():
            return HttpResponse("Plan already exists", status=400)

        try:
            price = Decimal(request.POST.get("price"))
        except (TypeError, ValueError):
            return HttpResponse("Invalid price", status=400)

        if price < 500:
            return HttpResponse("Price is too low", status=400)

        valid_durations = ["one_month", "three_months", "six_months", "twelve_months"]
        duration = request.POST.get("duration")

        if duration not in valid_durations:
            return HttpResponse("Invalid duration", status=400)

        try:
            sessions = int(request.POST.get("number_of_sessions") or 0)
        except ValueError:
            return HttpResponse("Invalid sessions", status=400)

        Plan.objects.create(
            branch=branch,
            plan_name=plan_name,
            price=price,
            duration=duration,
            number_of_sessions=sessions,
            number_of_spa_sessions=int(request.POST.get("number_of_spa_sessions") or 0),
            number_of_suana_sessions=int(request.POST.get("number_of_suana_sessions") or 0),
            number_of_jacuzzi_sessions=int(request.POST.get("number_of_jacuzzi_sessions") or 0),
        )

    return redirect("admin-panel")

@login_required
@admin_required
def delete_plan(request, plan_id):
    if request.method == "POST":
        plan = get_object_or_404(Plan, pk=plan_id)
        plan.delete()

    return redirect("admin-panel")
