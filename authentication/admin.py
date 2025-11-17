from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from authentication.models import CustomUser


@register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username','email', 'first_name', 'last_name', 'date_of_birth')

    fieldsets = UserAdmin.fieldsets + (
        ("Informations supplémentaires", {
            "fields": (
                "date_of_birth",
                "can_be_contacted",
                "can_data_be_shared",
            ),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informations supplémentaires", {
            "classes": ("wide",),
            "fields": (
                "date_of_birth",
                "can_be_contacted",
                "can_data_be_shared",
            ),
        }),
    )
