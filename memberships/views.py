from django.shortcuts import render
from django.http import HttpResponse
from .models import Branch, Plan
from users.models import User, TrainerProfile

def home_view(request):
    members = User.objects.filter(role="member")
    trainers = User.objects.filter(role="trainer")

    return render(request, "memberships/home.html", {"members": members, "trainers":trainers})
