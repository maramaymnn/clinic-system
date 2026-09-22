from django.conf import settings
from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]


    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patient_profile'
    )

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )
    date_of_birth = models.DateField(null=True, blank=True)

    is_online = models.BooleanField(default=False)

    subscription_start = models.DateField(null=True, blank=True)
    subscription_end = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return self.name

class InitialAssessment(models.Model):
    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('weight_gain', 'Weight Gain'),
        ('body_recomposition', 'Body Recomposition'),
        ('healthy_eating', 'Healthy Eating'),
    ]


    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name='assessment'
    )

    goal = models.CharField(
        max_length=30,
        choices=GOAL_CHOICES
    )

    eating_habits = models.TextField(blank=True)
    sleep = models.TextField(blank=True)
    activity_level = models.TextField(blank=True)
    previous_diets = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Client Intake'
        verbose_name_plural = 'Client Intakes'

    def __str__(self):
        return f"Intake - {self.patient.name}"

