from django.db import models

class DietPlan(models.Model):
    patient = models.ForeignKey(
        'patient_records.Patient',
        on_delete=models.CASCADE,
        related_name='diet_plans'
    )
    title = models.CharField(max_length=200)
    version = models.PositiveIntegerField(default=1)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    calories = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    pdf_file = models.FileField(
        upload_to='diet_plans/pdfs/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Nutrition Plan'
        verbose_name_plural = 'Nutrition Plans'
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.patient} - {self.title} - V{self.version}'

    def save(self, *args, **kwargs):
        if not self.pk:
            last_plan = (
                DietPlan.objects
                .filter(patient=self.patient)
                .order_by('-version')
                .first()
            )

            if last_plan:
                self.version = last_plan.version + 1
            else:
                self.version = 1

        super().save(*args, **kwargs)


class DietPlanImage(models.Model):
    diet_plan = models.ForeignKey(
        DietPlan,
        on_delete=models.CASCADE,
        related_name='meal_images'
    )
    image = models.ImageField(upload_to='diet_plans/meals/')
    grams = models.PositiveIntegerField(null=True, blank=True)
    substitutes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Meal Photo'
        verbose_name_plural = 'Meal Photos'
        ordering = ['created_at']

    def __str__(self):
        return f'Meal Photo - {self.diet_plan}'