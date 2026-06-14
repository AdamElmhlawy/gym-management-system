from django.urls import path
from .views import (admin_panel, promote_member, accept_trainer, fire_trainer, 
                    create_branch, delete_branch, create_plan, delete_plan)

urlpatterns = [
    path("", admin_panel, name="admin-panel"),
    path("member/promote/<int:user_id>" , promote_member, name="promote-member"),
    path("trainer/accept/<int:user_id>", accept_trainer, name="accept-trainer"),
    path("trainer/fire/<int:user_id>", fire_trainer, name="fire-trainer"),
    path("branch/create/", create_branch, name="create-branch"),
    path("branch/delete/<int:branch_id>", delete_branch, name="delete-branch"),
    path("plan/create/", create_plan, name="create-plan"),
    path("plan/delete/<int:plan_id>", delete_plan, name="delete-plan"),
]
