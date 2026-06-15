from django.db import models
from django.core.exceptions import ValidationError


class MemberTrainer(models.Model):
    member = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='member_trainers')
    trainer = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='trainer_members')
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

        if self.trainer.role != "trainer":
            raise ValidationError("trainers_must_have_role_'trainer'")

        if self.member_id == self.trainer_id:
            raise ValidationError("users_cannot_train_themselves")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.trainer.username} Trains {self.member.username} since {self.assigned_date}. ({self.is_active})"