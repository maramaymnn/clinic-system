from django import forms
from .models import ExercisePlan

class ExercisePlanForm(forms.ModelForm):
	class Meta:
		model = ExercisePlan
		fields = [
			'title',
			'plan_type',
			'start_date',
			'end_date',
			'notes',
			'pdf_file',
		]
		widgets = {
			'start_date': forms.DateInput(attrs={'type': 'date'}),
			'end_date': forms.DateInput(attrs={'type': 'date'}),
		}
