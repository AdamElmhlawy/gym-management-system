from django.urls import path
from .views import register, UserLoginView, UserLogoutView

urlpatterns = [
    path('signup/', register, name="signup"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name="logout"),
]
