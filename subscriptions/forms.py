from django import forms
from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = [
            'start_date',
            'end_date',
            'status',
            'notes',
        ]

        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'end_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }