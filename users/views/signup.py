from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db import transaction

from users.models import TrainerProfile
from users.forms import UserRegisterForm, UserInformationForm


def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        information_form = UserInformationForm(request.POST, request.FILES)

        if user_form.is_valid() and information_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                
                user_information = information_form.save(commit=False)
                user_information.user = user
                user_information.save()

                if request.POST.get("account_type") == "trainer":
                    user.role = "trainer"
                    user.save(update_fields=["role"])
                    TrainerProfile.objects.create(user=user)

                login(request, user)
                return redirect("home")
    else:
        user_form = UserRegisterForm()
        information_form = UserInformationForm()
    
    return render(request, "users/signup.html", {"user_form": user_form,
    "information_form": information_form,})