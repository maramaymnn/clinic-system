from django.contrib import admin
from .models import Progress


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'date',
        'weight',
        'body_fat',
        'muscle_mass',
        'water_percentage',
    )

    list_filter = (
        'date',
    )

    search_fields = (
        'patient__name',
        'patient__phone',
    )