from django.shortcuts import render, redirect, get_object_or_404

from patient_records.models import Patient
from .forms import ExercisePlanForm
from .models import ExercisePlan
from clinic_users.decorators import role_required


@role_required(['admin', 'exercise_coach'])
def create_exercise_plan(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = ExercisePlanForm(request.POST, request.FILES)

        if form.is_valid():
            exercise_plan = form.save(commit=False)
            exercise_plan.patient = patient
            exercise_plan.save()
            return redirect('patient_detail', patient_id=patient.id)

    else:
        form = ExercisePlanForm()

    return render(
        request,
        'exercise_plans/add_exercise_plan.html',
        {
            'form': form,
            'patient': patient,
        }
    )