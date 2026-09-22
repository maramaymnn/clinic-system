from django.db import models

from patient_records.models import Patient
from clinic_users.models import User


class Appointment(models.Model):

    STATUS_CHOICES = [
        ('awaiting_confirmation', 'Awaiting Confirmation'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('no_response', 'No Response'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    coach = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments'
    )

    date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default='awaiting_confirmation'
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.patient.name} - {self.date}"