from django.shortcuts import render
from django.http import HttpResponse
from .models import Branch, Plan
from users.models import User, TrainerProfile

def home_view(request):
    members = User.objects.filter(role="member")
    trainers = User.objects.filter(role="trainer")

    context = {
    "members": members,
    "trainers": trainers,
    "member_count": members.count(),
    "trainer_count": trainers.count(),
    "total_users": members.count() + trainers.count(),
    }

    return render(request, "memberships/home.html", context)
