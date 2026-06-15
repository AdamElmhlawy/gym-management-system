from django.shortcuts import redirect, get_object_or_404

from django.views import View
from django.views.generic import TemplateView
from .mixins import LoginAdminRequiredMixin

from users.models import User


class AdminUserView(LoginAdminRequiredMixin, TemplateView):
    template_name = "admin_panel/admin_user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        members = User.objects.filter(role="member").select_related("user_information")
        admins = User.objects.filter(role="admin").select_related("user_information")

        #-----------stats-------------#
        member_count = members.count()
        admin_count = admins.count()

        context = ({
            "members": members, "admins": admins, 
            "member_count": member_count, "admin_count": admin_count,
        })
        return context

class PromoteMemberView(LoginAdminRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.role = "admin"
        user.save()

        return redirect("admin-user")