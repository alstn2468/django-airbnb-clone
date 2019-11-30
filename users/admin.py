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
                )
            },
        ),
    )
    fieldsets = BaseUserAdmin.fieldsets + user_fieldsets
