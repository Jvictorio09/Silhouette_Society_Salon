from django.contrib import admin

from .models import SpaBooking


@admin.register(SpaBooking)
class SpaBookingAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "phone_number",
        "selected_service",
        "service_for",
        "preferred_date",
        "created_at",
    )
    list_filter = ("service_for", "selected_service", "preferred_date", "created_at")
    search_fields = ("full_name", "phone_number", "email_address", "selected_service")
