from django.shortcuts import redirect, get_object_or_404

from django.core.paginator import Paginator
from django.views import View
from django.views.generic import TemplateView
from .mixins import LoginAdminRequiredMixin

from users.models import User


class AdminUserView(LoginAdminRequiredMixin, TemplateView):
    template_name = "admins/user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        members = User.objects.filter(role="member").select_related("user_information").order_by("username")
        admins = User.objects.filter(role="admin").select_related("user_information").order_by("username")



        #-----------paginators-------------#
        member_paginator = Paginator(members, 10)
        member_page_number = self.request.GET.get("member_page")
        member_page = member_paginator.get_page(member_page_number)

        admin_paginator = Paginator(admins, 10)
        admin_page_number = self.request.GET.get("admin_page")
        admin_page = admin_paginator.get_page(admin_page_number)

        #-----------stats-------------#
        member_count = members.count()
        admin_count = admins.count()

        context = ({
            "members": member_page, "admins": admin_page, 
            "member_count": member_count, "admin_count": admin_count,
        })
        return context

class PromoteMemberView(LoginAdminRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.role = "admin"
        user.save()

        return redirect("admin-user")