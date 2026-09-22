from django.db import models
from patient_records.models import Patient
from django.conf import settings


class Notification(models.Model):
    TYPE_CHOICES = [
        ('subscription_expiry', 'Subscription Expiry'),
        ('follow_up', 'Follow-up'),
        ('appointment', 'Appointment'),
        ('general', 'General'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )
    recipient = models.ForeignKey(
settings.AUTH_USER_MODEL,
on_delete=models.CASCADE,
null=True,
blank=True,
related_name='notifications'
)


    title = models.CharField(max_length=200)

    message = models.TextField()

    notification_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        default='general'
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title