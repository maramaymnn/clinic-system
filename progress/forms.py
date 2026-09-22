from django import forms
from .models import Progress


class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = [
            'date',
            'weight',
            'body_fat',
            'muscle_mass',
            'water_percentage',
            'notes',
        ]

        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }