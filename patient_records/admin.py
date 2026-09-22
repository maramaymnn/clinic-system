from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'gender',
        'is_online',
        'subscription_start',
        'subscription_end',
        'status',
    )

    list_filter = (
        'gender',
        'is_online',
        'status',
    )

    search_fields = (
        'name',
        'phone',
        'email',
    )