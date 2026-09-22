from django import forms

from .models import DietPlan, DietPlanImage

class DietPlanForm(forms.ModelForm):

    class Meta:
        model = DietPlan
        fields = [
            'title',
            'start_date',
            'end_date',
            'calories',
            'notes',
            'pdf_file',
        ]
        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'end_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

class DietPlanImageForm(forms.ModelForm):


    class Meta:
        model = DietPlanImage
        fields = [
            'image',
            'grams',
            'substitutes',
        ]
