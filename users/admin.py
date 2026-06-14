from django.contrib import admin
from .models import (
    User,
    UserInformation,
    TrainerProfile,
    MemberTrainer,
)


# USER INFORMATION INLINE
class UserInformationInline(admin.StackedInline):
    model = UserInformation
    can_delete = False
    verbose_name_plural = "User Information"
    fields = ("profile_pic", "phone_number", "gender", "date_of_birth", "branch")


# USER ADMIN
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_staff")
    search_fields = ("username", "email")
    list_filter = ("role",)

    fieldsets = (
        ("Account Info", {
            "fields": ("username", "email", "password")
        }),
        ("Role & Permissions", {
            "fields": ("role", "is_staff", "is_active")
        }),
    )

    inlines = [UserInformationInline]


# TRAINER PROFILE ADMIN
@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "salary", "years_of_experience")
    search_fields = ("user__username",)
    list_filter = ("years_of_experience",)

    fieldsets = (
        ("Trainer Info", {
            "fields": ("user", "salary", "years_of_experience")
        }),
    )


# MEMBER - TRAINER RELATION
@admin.register(MemberTrainer)
class MemberTrainerAdmin(admin.ModelAdmin):
    list_display = ("member", "trainer", "assigned_date", "is_active")
    list_filter = ("is_active",)
    search_fields = ("member__username", "trainer__username")

    fieldsets = (
        ("Assignment", {
            "fields": ("member", "trainer", "is_active")
        }),
    )