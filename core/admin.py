from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.site_header = "Rest Market Main Administration"
admin.site.index_title = "Admin Panel Overview"


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    """Django admin interface of users"""

    fieldsets = (
        (None, {"fields": ("email", "password", "username", "phone_number")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "phone_number",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    list_display = [
        "id",
        "email",
        "username",
        "phone_number",
        "is_active",
        "is_staff",
        "is_superuser",
    ]

    ordering = ["id"]
    search_fields = ["username"]
    list_per_page = 16
