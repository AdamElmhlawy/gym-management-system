from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator


class Plan(models.Model):
    Duration_Choices = [
        ("one_month", "One_Month"),
        ("three_months", "Three_Months"),
        ("six_months", "Six_Months"),
        ("twelve_months", "Twelve_Months")
    ]

    branch = models.ForeignKey("members.Branch", on_delete=models.CASCADE, related_name='branch_plans')
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