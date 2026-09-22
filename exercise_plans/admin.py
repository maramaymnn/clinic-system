from django.contrib import admin
from .models import ExercisePlan


@admin.register(ExercisePlan)
class ExercisePlanAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'title',
        'plan_type',
        'start_date',
        'end_date',
        'created_at',
    )

    list_filter = (
        'plan_type',
        'start_date',
        'end_date',
    )

    search_fields = (
        'patient__name',
        'patient__phone',
        'title',
    )