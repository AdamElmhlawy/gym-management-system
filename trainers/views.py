from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import TrainerProfile

class TrainerProfileCreateView(LoginRequiredMixin, CreateView):
    model = TrainerProfile
    template_name = "create_trainer_profile.html"
    fields = []
    success_url = reverse_lazy("home")  # replace "home" with your URL name

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
