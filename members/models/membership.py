from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

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
    plan = models.ForeignKey("members.Plan", on_delete=models.CASCADE, related_name="membership_plan")
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

        durations = {
            "one_month": 30, "three_months": 90, 
            "six_months": 180, "twelve_months": 360,
        }

        self.end_date = (
            self.start_date + timedelta(days=durations.get(self.plan.duration, 0))
        )

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