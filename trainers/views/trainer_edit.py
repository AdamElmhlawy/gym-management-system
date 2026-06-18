from django.urls import reverse
from admins.views.mixins import LoginAdminRequiredMixin
from django.views.generic import DetailView, UpdateView

from users.models import TrainerProfile
from users.forms import TrainerProfileForm

class TrainerDetailView(DetailView):
    template_name = "trainers/trainer_detail.html"
    model = TrainerProfile
    context_object_name = "trainer"
    
    slug_field = "user_id"
    slug_url_kwarg = "user_id"

class TrainerUpdateView(LoginAdminRequiredMixin, UpdateView):
    template_name = "trainers/trainer_update.html"
    model = TrainerProfile
    context_object_name = "trainer"
    form_class = TrainerProfileForm

    slug_field = "user_id"
    slug_url_kwarg = "user_id"

    def get_success_url(self):
        return reverse("trainer-detail", kwargs={"user_id": self.object.user_id})



    