from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register, ProfileView, ProfileEditView

urlpatterns = [
    path('signup/', register, name="signup"),
    path('login/', LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', LogoutView.as_view(next_page="login"), name="logout"),
    path('profile', ProfileView.as_view(), name="profile"),
    path('profile/edit', ProfileEditView.as_view(), name="profile-edit"),
]
