from django.db import models
from patient_records.models import Patient


class ExercisePlan(models.Model):

    PLAN_TYPE_CHOICES = [
        ('home', 'Home'),
        ('gym', 'Gym'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='exercise_plans'
    )

    title = models.CharField(max_length=200)

    plan_type = models.CharField(
        max_length=10,
        choices=PLAN_TYPE_CHOICES
    )

    version = models.PositiveIntegerField(default=1)

    start_date = models.DateField()
    end_date = models.DateField()

    notes = models.TextField(blank=True)

    pdf_file = models.FileField(
        upload_to='exercise_plans/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Workout Plan'
        verbose_name_plural = 'Workout Plans'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.patient.name} - {self.title} (v{self.version})"

    def save(self, *args, **kwargs):
        if not self.pk and not self.version:
            last = ExercisePlan.objects.filter(
                patient=self.patient
            ).order_by('-version').first()
            self.version = (last.version + 1) if last else 1
        super().save(*args, **kwargs)