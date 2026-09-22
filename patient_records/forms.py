from django import forms

from .models import Patient, InitialAssessment


class PatientForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = Patient
        fields = [
            'name',
            'phone',
            'email',
            'gender',
            'date_of_birth',
            'is_online',
            'subscription_start',
            'subscription_end',
            'status',
            'notes',
        ]


class InitialAssessmentForm(forms.ModelForm):
    class Meta:
        model = InitialAssessment
        fields = [
            'goal',
            'eating_habits',
            'sleep',
            'activity_level',
            'previous_diets',
            'challenges',
            'notes',
        ]