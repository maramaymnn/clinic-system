from django.shortcuts import render, redirect, get_object_or_404

from clinic_users.decorators import role_required

from .models import Progress
from .forms import ProgressForm
from patient_records.models import Patient

@role_required(['admin', 'diet_doctor'])
def progress_list(request):


    progress_records = Progress.objects.select_related(
        'patient'
    ).order_by(
        '-date'
    )

    return render(
        request,
        'progress/progress_list.html',
        {
            'progress_records': progress_records,
        }
    )

@role_required(['admin', 'diet_doctor'])
def create_progress(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    if request.method == 'POST':

        form = ProgressForm(request.POST)

        if form.is_valid():

            progress = form.save(commit=False)
            progress.patient = patient
            progress.save()

            return redirect(
                'patient_detail',
                patient_id=patient.id
            )

    else:

        form = ProgressForm()

    return render(
        request,
        'progress/add_progress.html',
        {
            'form': form,
            'patient': patient,
        }
    )
