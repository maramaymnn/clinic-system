from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('receptionist', 'Receptionist'),
        ('diet_doctor', 'Nutrition Specialist'),
        ('exercise_coach', 'Fitness Coach'),
        ('follow_up', 'Follow-up Doctor'),
        ('client', 'Client'),
    ]


    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default='receptionist'
    )

    def __str__(self):
        return self.username
