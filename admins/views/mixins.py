from django.core.exceptions import PermissionDenied

class LoginAdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.role != "admin":
            raise PermissionDenied("Admins only.")

        return super().dispatch(request, *args, **kwargs)