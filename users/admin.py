from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Register User model at admin panel
    Set fieldsets BaseUserAdmin's fieldsets + user_fieldsets
    
    Inherit:
        UserAdmin as BaseUserAdmin

    user_fieldsets : Custom User model's fieldsets
    """

    user_fieldsets = (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birth_date",
                    "language",
                    "currency",
                    "is_superhost",
                    "login_method",
                )
            },
        ),
    )
    fieldsets = BaseUserAdmin.fieldsets + user_fieldsets

    list_filter = BaseUserAdmin.list_filter + ("is_superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "is_superhost",
        "is_staff",
        "is_superuser",
        "login_method",
    )
