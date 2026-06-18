from django.views.generic import ListView
from members.models import Branch

class BranchListView(ListView):
    template_name = "members/branches.html"
    model = Branch
    context_object_name = "branches"
    ordering = ["branch_name"]
    paginate_by = 5
