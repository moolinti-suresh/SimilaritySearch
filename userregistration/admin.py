from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = (
        "user_id",
        "username",
        "city",
        "state",
        "country",
        "pin",
        "full_address",
        "aadhaar_file",
        "eb_bill_file",
    )

    search_fields = (
        "user_id",
        "username",
        "city",
    )

    ordering = ("user_id",)