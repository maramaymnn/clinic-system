from django.db import models
from patient_records.models import Patient


class Progress(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='progress_records'
    )

    date = models.DateField()

    weight = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    body_fat = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    muscle_mass = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    water_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Body Analysis'
        verbose_name_plural = 'Body Analysis Records'
        ordering = ['-date']

    def __str__(self):
        return f"{self.patient.name} - {self.date}"