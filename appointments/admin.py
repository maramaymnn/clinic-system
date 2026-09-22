from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'coach',
        'date',
        'start_time',
        'end_time',
    )

    list_filter = (
        'date',
        'coach',
    )

    search_fields = (
        'patient__name',
        'patient__phone',
        'coach__username',
    )