from django.db import models
from patient_records.models import Patient


class FollowUp(models.Model):
    STATUS_CHOICES = [
        ('doing_well', 'Doing Well'),
        ('review', 'Review'),
        ('needs_attention', 'Needs Attention'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='follow_ups'
    )

    date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='doing_well'
    )

    meals = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    replacement_request = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Daily Check-in'
        verbose_name_plural = 'Daily Check-ins'
        ordering = ['-date']

    def __str__(self):
        return f"{self.patient.name} - {self.date}"