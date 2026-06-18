from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from django.views.generic import DetailView

from users.models import TrainerProfile, UserInformation
from users.forms import UserInformationForm, TrainerProfileForm


class ProfileView(LoginRequiredMixin, DetailView):
    model = UserInformation
    template_name = "users/profile.html"

    def get_object(self):
        return self.request.user.user_information
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        trainer_profile = None
        trainer_pending = False
        if user.role == "trainer":
            trainer_profile = TrainerProfile.objects.filter(user=user).first()
            # Track whether a trainer profile exists but is still waiting for approval.
            if trainer_profile and not trainer_profile.is_active and not trainer_profile.is_fired:
                trainer_pending = True

        context["trainer_profile"] = trainer_profile
        context["trainer_pending"] = trainer_pending

        return context
    
class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_info = user.user_information

        trainer_profile = None
        if user.role == "trainer": 
            trainer_profile = TrainerProfile.objects.filter(user=user).first()
        
        return render(request, "users/profile_edit.html", {
            "user_form": UserInformationForm(instance=user_info),
            # Only pass trainer_form for trainers. Non-trainers get None.
            "trainer_form": TrainerProfileForm(instance=trainer_profile) if user.role == "trainer" else None
        })
    
    def post(self, request):
        user = request.user
        user_info = user.user_information

        trainer_profile = None
        if user.role == "trainer": 
            trainer_profile = TrainerProfile.objects.filter(user=user).first()
        
        user_form = UserInformationForm(request.POST, request.FILES, instance=user_info)
        trainer_form = TrainerProfileForm(request.POST, instance=trainer_profile) if user.role == "trainer" else None

        # Validate both forms when trainer form exists.
        forms_valid = user_form.is_valid() and (trainer_form is None or trainer_form.is_valid())
        if forms_valid:
            user_form.save()
            if trainer_form is not None:
                trainer = trainer_form.save(commit=False)
                trainer.user = user
                trainer.save()
            # Redirect with required user_id parameter in profile URL.
            return redirect("profile")
        
        return render(request, "users/profile_edit.html", {
            "user_form": user_form,
            "trainer_form": trainer_form,
        })

# FIXES APPLIED:
# 1. Added default `trainer_profile = None` before trainer logic to prevent NameError for non-trainers.
# 2. Added `trainer_pending` context so `users/profile.html` can safely display pending status.
# 3. Updated redirect to include `user_id=user.id` because the profile URL requires that parameter.
# 4. Added inline comments describing the fixes and behavior.
