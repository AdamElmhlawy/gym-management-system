from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class User(AbstractUser):
    Role_Choices = [
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('trainer', 'Trainer'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role_Choices, default='member')
    #branch = models.ManyToManyField()
    phone_number = models.CharField(max_length=15, blank=False, null=False, unique=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=False, null=False)
    date_of_birth = models.DateField(blank=False, null=False, help_text="Format: YYYY-MM-DD")
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    salary = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('5000.0'))],
                                blank = False, null = False)
    years_of_experience = models.PositiveIntegerField()

    def clean(self):
        if not self.user:
            raise ValidationError("Trainer must have a user")
        
        if self.user.role != "trainer":
            raise ValidationError("User must have role 'trainer' to have a trainer profile")
        
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
        if not self.member_id or not self.trainer_id:
            raise ValidationError("Member and trainer are required")

        member = self.member
        trainer = self.trainer

        if member.role != "member":
            raise ValidationError("Members must have role 'member'")

        if trainer.role != "trainer":
            raise ValidationError("Trainers must have role 'trainer'")

        if self.member_id == self.trainer_id:
            raise ValidationError("Users cannot train themselves")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.trainer.username} Trains {self.member.username} since {self.assigned_date}. ({self.is_active})"
    