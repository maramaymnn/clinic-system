from django.shortcuts import render, redirect, get_object_or_404

from clinic_users.decorators import role_required

from .forms import AppointmentForm
from .models import Appointment
from patient_records.models import Patient


@role_required([
    'admin',
    'receptionist',
    'exercise_coach'
])
def create_appointment(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    if request.method == 'POST':
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()

            return redirect(
                'patient_detail',
                patient_id=patient.id
            )
    else:
        form = AppointmentForm()

    return render(
        request,
        'appointments/add_appointment.html',
        {
            'form': form,
            'patient': patient,
        }
    )


@role_required([
    'admin',
    'receptionist',
    'exercise_coach'
])
def appointments_list(request):

    appointments = Appointment.objects.select_related(
        'patient',
        'coach'
    ).order_by(
        'date',
        'start_time'
    )

    return render(
        request,
        'appointments/appointments_list.html',
        {
            'appointments': appointments,
        }
    )


@role_required([
    'admin',
    'receptionist'
])
def update_appointment_status(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    status = request.POST.get('status')

    valid_statuses = [
        'confirmed', 'cancelled', 'no_response', 'awaiting_confirmation'
    ]

    if status in valid_statuses:
        appointment.status = status
        appointment.save(update_fields=['status'])

    return redirect('appointments')