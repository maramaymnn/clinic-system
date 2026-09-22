from django.contrib import admin
from .models import DietPlan


@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'title',
        'start_date',
        'end_date',
        'calories',
        'created_at',
    )

    list_filter = (
        'start_date',
        'end_date',
    )

    search_fields = (
        'patient__name',
        'patient__phone',
        'title',
    )