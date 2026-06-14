from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

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
    branch = models.ForeignKey("memberships.Branch", on_delete=models.CASCADE, related_name='user_branch')
    phone_number = models.CharField(max_length=15, blank=False, null=False, unique=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=False, null=False)
    date_of_birth = models.DateField(blank=False, null=False, help_text="Format: YYYY-MM-DD")
    join_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.user.role})"

class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    salary = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('5000.0'))],)
    years_of_experience = models.PositiveIntegerField(default=0)

    def clean(self):
        if self.user.role != "trainer":
            raise ValidationError("user_must_have_role_'trainer'_to_have_a_trainer_profile")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Trainer {self.user.username} have {self.years_of_experience} years of experience" 

class MemberTrainer(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member_trainers')
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainer_members')
    assigned_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
            fields=["member"],
            condition=models.Q(is_active=True),
            name = "one_active_trainer_per_member"),
            models.UniqueConstraint(
                fields=["member", "trainer"],
                name = "unique_member_trainer_pair"
            )
        ]
    
    def clean(self):
        if self.trainer.user_information.branch_id !=self.member.user_information.branch_id:
            raise ValidationError("Trainer must be from same branch")

        if self.member.role != "member":
            raise ValidationError("members_must_have_role_'member'")

        if self.trainer != "trainer":
            raise ValidationError("trainers_must_have_role_'trainer'")

        if self.member_id == self.trainer_id:
            raise ValidationError("users_cannot_train_themselves")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.trainer.username} Trains {self.member.username} since {self.assigned_date}. ({self.is_active})"
    