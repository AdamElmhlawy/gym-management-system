from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Branch(models.Model):
    Cities = [
        ("tanta", "Tanta"),
        ("cairo", "Cairo"),
        ("alexandria", "Alexandria"),
        ("mansura", "Mansura"),
        ("suez", "Suez"),
        ("north_sinai", "North_Sinai"),
        ("boston", "Boston"),
        ("london", "London"),
        ("berlin", "Berlin"),
        ("barcelona", "Barcelona"),
        ("moscow", "Moscow"),
        ("stockholm", "Stockholm")
    ]
    branch_name = models.CharField(max_length=100, unique=True, default="cario")
    city = models.CharField(max_length=100, blank=False, null=False, choices=Cities)

    def __str__(self):
        return f"{self.branch_name} in {self.city} city"


class Plan(models.Model):
    Duration_Choices = [
        ("one_month", "One_Month"),
        ("three_months", "Three_Months"),
        ("six_months", "Six_Months"),
        ("twelve_months", "Twelve_Months")
    ]

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_plans')
    plan_name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('500.0'))],)
    duration = models.CharField(max_length=20, choices=Duration_Choices, default="one_month")
    number_of_sessions = models.PositiveIntegerField(default=10)
    number_of_spa_sessions = models.PositiveIntegerField(default=0)
    number_of_suana_sessions = models.PositiveIntegerField(default=0)
    number_of_jacuzzi_sessions = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.plan_name} for {self.branch.branch_name} for {self.duration}"
    

class MemberShip(models.Model):
    Payment_Choices = [
        ("cash", "Cash"),
        ("visa", "Visa"),
        ("wallet", "Wallet")
    ]
    Status_Choices = [
        ("active", "Active"),
        ("expired", "Expired"),
        ("paused", "Paused"),
    ]
    member = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="member_memberships")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="membership_plan")
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.0'))],)
    payment_method = models.CharField(max_length=20, choices=Payment_Choices, default="cash")
    status = models.CharField(max_length=20, choices=Status_Choices, default="active")

    def clean(self):
        if self.member.role != "member":
            raise ValidationError("user_must_have_role_member")
        
    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = timezone.now().date()

        if self.plan.duration == "one_month":
            self.end_date = self.start_date + timedelta(days=30)

        elif self.plan.duration == "three_months":
            self.end_date = self.start_date + timedelta(days=90)

        elif self.plan.duration == "six_months":
            self.end_date = self.start_date + timedelta(days=180)

        elif self.plan.duration == "twelve_months":
            self.end_date = self.start_date + timedelta(days=360)
        
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.member.username}'s membership until {self.end_date}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
            fields=["member"],
            condition=models.Q(status__in=["active", "paused"]),
            name = "one_active_membership_per_member")
        ]


class MemberShipUsage(models.Model):
    membership = models.OneToOneField(MemberShip, on_delete=models.CASCADE, related_name="membership_usage")
    sessions_used = models.PositiveIntegerField(default=0)
    spa_sessions_used = models.PositiveIntegerField(default=0)
    suana_sessions_used =models.PositiveIntegerField(default=0)
    jacuzzi_sessions_used =models.PositiveIntegerField(default=0)