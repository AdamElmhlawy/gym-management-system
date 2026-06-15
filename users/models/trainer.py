from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class TrainerProfile(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name='trainer_profile')
    is_active = models.BooleanField(default=False)
    is_fired = models.BooleanField(default=False)
    salary = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.0'))],)
    years_of_experience = models.PositiveIntegerField(default=0)

    def clean(self):
        if self.user.role != "trainer":
            raise ValidationError("user_must_have_role_'trainer'_to_have_a_trainer_profile")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Trainer {self.user.username} have {self.years_of_experience} years of experience" 
