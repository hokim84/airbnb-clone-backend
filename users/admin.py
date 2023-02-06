from dataclasses import fields
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models  import User

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "Profile", 
            {
                "fields": (
                    "avatar","real_name", 
                    "username", "password", "name",
                    "email", "is_host", "language", "currency"),
            },
            
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important_Dates",
            {
                "fields" : (
                    "last_login", "date_joined"
                ),
            },
        )
    )
    
    list_display = ("username", "email", "name")