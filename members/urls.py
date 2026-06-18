from django.urls import path
from .views import HomeListView, BranchListView, PlanListView

urlpatterns = [
    path("", HomeListView.as_view(), name="home"),
    path("branches/", BranchListView.as_view(), name="branch-list"),
    path("plans/", PlanListView.as_view(), name="plan-list"),
]