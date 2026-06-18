from django.views.generic import ListView
from members.models import Plan

class PlanListView(ListView):
    template_name = "members/plans.html"
    model = Plan
    context_object_name = "plans"
    ordering = ["branch"]
    paginate_by = 5