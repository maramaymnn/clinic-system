from django import forms
from .models import FollowUp


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = [
            'date',
            'status',
            'meals',
            'replacement_request',
            'notes',
        ]

        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }