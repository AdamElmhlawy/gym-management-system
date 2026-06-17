from django.core.paginator import Paginator

from django.views.generic import TemplateView

from .models import Plan
from users.models import User, TrainerProfile


class HomeListView(TemplateView):
    template_name = "members/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        members = User.objects.filter(role="member"
        ).select_related("user_information").order_by("username")

        trainers = TrainerProfile.objects.filter(is_active=True
        ).select_related("user", "user__user_information").order_by("years_of_experience")

        #-----------paginators-------------#
        member_paginator = Paginator(members, 4)
        member_page_number = self.request.GET.get("member_page")
        member_page = member_paginator.get_page(member_page_number)

        trainer_paginator = Paginator(trainers, 4)
        trainer_page_number = self.request.GET.get("trainer_page")
        trainer_page = trainer_paginator.get_page(trainer_page_number)

        #-----------stats-------------#
        member_count = members.count()
        trainer_count = trainers.count()

        context = {
            "members": member_page, "member_count": member_count,
            "trainers": trainer_page, "trainer_count": trainer_count,
            "total_users": member_count + trainer_count, "plan_count": Plan.objects.count(),
        }
        return context