from django.contrib import admin
from .models import FollowUp


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'date',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'date',
    )

    search_fields = (
        'patient__name',
        'patient__phone',
    )