from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserInformationForm
from django.db import transaction
from django.contrib.auth import login


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

                login(request, user)
                return redirect("home")
    else:
        user_form = UserRegisterForm()
        information_form = UserInformationForm()
    
    return render(request, "users/signup.html", {"user_form": user_form,
                                                  "information_form": information_form,})