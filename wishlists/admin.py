from django.contrib import admin
from .models import WishList

# Register your models here.
@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "created_at",
        "updated_at",
    )
