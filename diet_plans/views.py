from django.shortcuts import render, redirect, get_object_or_404

from clinic_users.decorators import role_required

from .models import DietPlan, DietPlanImage
from .forms import DietPlanForm
from patient_records.models import Patient


@role_required(['admin', 'diet_doctor'])
def create_diet_plan(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    if request.method == 'POST':

        form = DietPlanForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            diet_plan = form.save(commit=False)
            diet_plan.patient = patient
            diet_plan.save()

            # Multiple meal photos (grams + substitutes) can be
            # attached at once via <input type="file" multiple>.
            for image_file in request.FILES.getlist('meal_images'):
                DietPlanImage.objects.create(
                    diet_plan=diet_plan,
                    image=image_file
                )

            return redirect(
                'patient_detail',
                patient_id=patient.id
            )

    else:

        form = DietPlanForm()

    return render(
        request,
        'diet_plans/add_diet_plan.html',
        {
            'form': form,
            'patient': patient,
        }
    )