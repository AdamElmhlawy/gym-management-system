from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    Roles = [
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('trainer', 'Trainer'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Roles, default='member')

    def __str__(self):
        return f"{self.username} ({self.role})"

class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_information')
    profile_pic = models.ImageField(upload_to="profile_pics/",
                                      default="defaults/default_profile.png")
    branch = models.ForeignKey("members.Branch", on_delete=models.CASCADE, related_name='user_branch')
    phone_number = models.CharField(max_length=15, blank=False, null=False, unique=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=False, null=False)
    date_of_birth = models.DateField(blank=False, null=False, help_text="Format: YYYY-MM-DD")
    join_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.user.role})"