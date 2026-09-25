from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_id",
        "full_name",
        "email",
        "department",
        "designation",
        "status",
        "joining_date",
    )
    search_fields = ("employee_id", "first_name", "last_name", "email")
    list_filter = ("department", "status", "gender", "designation")
    list_select_related = ("department",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 25

    fieldsets = (
        ("Personal information", {
            "fields": (
                "employee_id", "first_name", "last_name", "email", "phone",
                "gender", "date_of_birth", "address", "profile_photo",
            )
        }),
        ("Employment information", {
            "fields": (
                "department", "designation", "salary", "joining_date", "status",
            )
        }),
        ("System information", {
            "fields": ("created_at", "updated_at"),
        }),
    )

    @admin.display(description="Employee name", ordering="first_name")
    def full_name(self, employee):
        return f"{employee.first_name} {employee.last_name}"

# Register your models here.
