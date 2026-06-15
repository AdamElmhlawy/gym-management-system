from django.contrib import admin
from .models import Branch, Plan, MemberShip, MemberShipUsage

# BRANCH ADMIN
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("branch_name", "city")
    search_fields = ("branch_name", "city")
    list_filter = ("city",)

    fieldsets = (
        ("Branch Info", {
            "fields": ("branch_name", "city")
        }),
    )


# PLAN ADMIN
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "plan_name",
        "branch",
        "price",
        "duration",
        "number_of_sessions",
        "number_of_spa_sessions",
        "number_of_suana_sessions",
        "number_of_jacuzzi_sessions",
    )

    list_filter = ("duration", "branch")
    search_fields = ("plan_name", "branch__branch_name")

    fieldsets = (
        ("Basic Info", {
            "fields": ("plan_name", "branch", "price", "duration")
        }),
        ("Sessions", {
            "fields": (
                "number_of_sessions",
                "number_of_spa_sessions",
                "number_of_suana_sessions",
                "number_of_jacuzzi_sessions",
            )
        }),
    )


# MEMBERSHIP ADMIN
@admin.register(MemberShip)
class MemberShipAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "plan",
        "status",
        "payment_method",
        "amount_paid",
        "start_date",
        "end_date",
    )

    list_filter = ("status", "payment_method")
    search_fields = ("member__username", "plan__plan_name")

    readonly_fields = ("start_date", "end_date")

    fieldsets = (
        ("Core Info", {
            "fields": ("member", "plan", "status")
        }),
        ("Payment", {
            "fields": ("amount_paid", "payment_method")
        }),
        ("Dates", {
            "fields": ("start_date", "end_date")
        }),
    )


# MEMBERSHIP USAGE ADMIN
@admin.register(MemberShipUsage)
class MemberShipUsageAdmin(admin.ModelAdmin):
    list_display = (
        "membership",
        "sessions_used",
        "spa_sessions_used",
        "suana_sessions_used",
        "jacuzzi_sessions_used",
    )

    search_fields = ("membership__member__username",)