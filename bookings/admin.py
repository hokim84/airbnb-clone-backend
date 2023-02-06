from django.contrib import admin
from .models import Booking

# Register your bmodels here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "kind",
        "user",
        "room",
        "experience",
        "check_in",
        "check_out",
        "experience_time",
        "guest",
    )

    list_filter = ("kind",)
