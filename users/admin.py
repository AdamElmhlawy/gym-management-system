from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserInformation, TrainerProfile, MemberTrainer


class UserInformationInline(admin.StackedInline):
    model = UserInformation
    can_delete = False
    extra = 0
    fields = (
        "profile_pic",
        "phone_number",
        "gender",
        "date_of_birth",
        "branch",
    )
    autocomplete_fields = ("branch",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_active")
    search_fields = ("username", "email")
    list_filter = ("role", "is_staff", "is_active")

    ordering = ("username",)

    fieldsets = (
        ("Account", {
            "fields": ("username", "email", "password")
        }),
        ("Role & Status", {
            "fields": ("role", "is_staff", "is_active")
        }),
        ("Permissions", {
            "fields": ("groups", "user_permissions")
        }),
    )

    inlines = [UserInformationInline]


@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "salary",
        "years_of_experience",
        "is_active",
        "is_fired",
    )

    list_filter = ("is_active", "is_fired", "years_of_experience")
    search_fields = ("user__username",)

    autocomplete_fields = ("user",)

    ordering = ("-years_of_experience",)

    fieldsets = (
        ("Trainer Status", {
            "fields": ("user", "is_active", "is_fired")
        }),
        ("Professional Info", {
            "fields": ("salary", "years_of_experience")
        }),
    )


@admin.register(MemberTrainer)
class MemberTrainerAdmin(admin.ModelAdmin):
    list_display = ("member", "trainer", "assigned_date", "is_active")

    list_filter = ("is_active",)
    search_fields = ("member__username", "trainer__username")

    autocomplete_fields = ("member", "trainer")

    ordering = ("-assigned_date",)

    fieldsets = (
        ("Assignment", {
            "fields": ("member", "trainer", "is_active")
        }),
    )