from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'start_date',
        'end_date',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'start_date',
        'end_date',
    )

    search_fields = (
        'patient__name',
        'patient__phone',
    )