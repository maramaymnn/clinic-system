from django.db import models
from patient_records.models import Patient

class Subscription(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Membership'
        verbose_name_plural = 'Memberships'
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.patient.name} - {self.start_date} to {self.end_date}'
