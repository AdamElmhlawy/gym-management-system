from .dashboard import AdminDashboardView
from .trainers import AdminActiveTrainerView
from .inactive_trainers import AdminFiredTrainerView, AdminPendingTrainerView
from .trainers_ops import HireTrainerView, FireTrainerView
from .users import AdminUserView, PromoteMemberView
from .branch_plan import (AdminBranchPlanView, 
                          BranchCreateView, 
                          BranchDeleteView, 
                          PlanCreateView, 
                          PlanDeleteView
                          )