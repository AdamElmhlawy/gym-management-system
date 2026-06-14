from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from decimal import Decimal
from users.models import User, TrainerProfile
from memberships.models import Branch, Plan, MemberShip
from django.db.models import Sum
from functools import wraps


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
    # 1. Security check (only admins allowed)
    if request.user.role != "admin":
        raise PermissionDenied("Only admins can access this endpoint.")

    # 2. Load data from database
    admins = User.objects.filter(role="admin").select_related("user_information")
    members = User.objects.filter(role="member").select_related("user_information")
    trainers = TrainerProfile.objects.select_related("user", "user__user_information")

    branches = Branch.objects.all()
    plans = Plan.objects.select_related("branch")

    # 3. Stats (numbers on top of page)
    admin_count = admins.count()
    member_count = members.count()
    trainer_count = trainers.filter(is_active=True).count()
    pending_trainer_count = trainers.filter(is_active=False, is_fired=False).count()
    fired_trainer_count = trainers.filter(is_fired=True).count()

    branch_count = branches.count()
    plan_count = plans.count()

    total_income = 0
    for m in members:
        if hasattr(m, "member_memberships"):
            total_income += sum(mm.amount_paid for mm in m.member_memberships.all())

    total_salaries = sum(t.salary for t in trainers if t.is_active)

    # 4. Search dataset (frontend search box uses this)
    people_json = []

    for u in admins:
        people_json.append({
            "id": u.id,
            "name": u.get_full_name() or u.username,
            "email": u.email,
            "role": "admin"
        })

    for u in members:
        people_json.append({
            "id": u.id,
            "name": u.get_full_name() or u.username,
            "email": u.email,
            "role": "member"
        })

    for t in trainers:
        people_json.append({
            "id": t.user.id,
            "name": t.user.get_full_name() or t.user.username,
            "email": t.user.email,
            "role": "trainer"
        })

    # 5. Send everything to template
    return render(request, "admin_panel/admin_panel.html", {
        "admins": admins,
        "members": members,
        "active_trainers": trainers.filter(is_active=True),
        "pending_trainers": trainers.filter(is_active=False, is_fired=False),
        "fired_trainers": trainers.filter(is_fired=True),

        "branches": branches,
        "plans": plans,

        # stats
        "admin_count": admin_count,
        "member_count": member_count,
        "trainer_count": trainer_count,
        "pending_trainer_count": pending_trainer_count,
        "fired_trainer_count": fired_trainer_count,
        "branch_count": branch_count,
        "plan_count": plan_count,
        "total_income": total_income,
        "total_salaries": total_salaries,

        # search system
        "people_json": people_json,
    })

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
