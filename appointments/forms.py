from django import forms

from .models import Appointment
from clinic_users.models import User


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment

        fields = [
            'coach',
            'date',
            'start_time',
            'end_time',
            'notes',
        ]

        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'start_time': forms.TimeInput(
                attrs={
                    'type': 'time'
                }
            ),

            'end_time': forms.TimeInput(
                attrs={
                    'type': 'time'
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['coach'].queryset = User.objects.filter(
            role__in=[
                'diet_doctor',
                'exercise_coach',
            ]
        ).order_by(
            'role',
            'username'
        )

        self.fields['coach'].label = 'Coach / Doctor'

        self.fields['coach'].empty_label = 'Select Coach / Doctor'