from django.shortcuts import render, redirect, get_object_or_404

from clinic_users.decorators import role_required

from .models import Patient, InitialAssessment
from .forms import PatientForm, InitialAssessmentForm

from subscriptions.models import Subscription
from diet_plans.models import DietPlan
from exercise_plans.models import ExercisePlan
from follow_ups.models import FollowUp
from progress.models import Progress
from appointments.models import Appointment


@role_required([
    'admin',
    'receptionist',
    'diet_doctor',
    'exercise_coach',
    'follow_up'
])
def patients(request):

    patients = Patient.objects.all().order_by('-created_at')

    context = {
        'patients': patients,
    }

    return render(
        request,
        'patient_records/patients.html',
        context
    )


@role_required(['admin', 'receptionist'])
def create_patient(request):

    if request.method == 'POST':
        form = PatientForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('patients')
    else:
        form = PatientForm()

    return render(
        request,
        'patient_records/add_patient.html',
        {
            'form': form
        }
    )


@role_required([
    'admin',
    'receptionist',
    'diet_doctor',
    'exercise_coach',
    'follow_up'
])
def patient_detail(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    subscriptions = Subscription.objects.filter(
        patient=patient
    ).order_by('-start_date')

    diet_plans = DietPlan.objects.filter(
        patient=patient
    ).prefetch_related('meal_images').order_by('-start_date')

    exercise_plans = ExercisePlan.objects.filter(
        patient=patient
    ).order_by('-start_date')

    follow_ups = FollowUp.objects.filter(
        patient=patient
    ).order_by('-date')

    progress_records = Progress.objects.filter(
        patient=patient
    ).order_by('-date')

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by('-date', '-start_time')

    context = {
        'patient': patient,
        'subscriptions': subscriptions,
        'diet_plans': diet_plans,
        'exercise_plans': exercise_plans,
        'follow_ups': follow_ups,
        'progress_records': progress_records,
        'appointments': appointments,
    }

    return render(
        request,
        'patient_records/patient_detail.html',
        context
    )


@role_required(['admin', 'receptionist'])
def create_assessment(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    assessment = InitialAssessment.objects.filter(
        patient=patient
    ).first()

    if request.method == 'POST':
        form = InitialAssessmentForm(
            request.POST,
            instance=assessment
        )

        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.patient = patient
            assessment.save()

            return redirect(
                'patient_detail',
                patient_id=patient.id
            )
    else:
        form = InitialAssessmentForm(
            instance=assessment
        )

    return render(
        request,
        'patient_records/add_assessment.html',
        {
            'form': form,
            'patient': patient,
            'assessment': assessment,
        }
    )
