from django.shortcuts import render, redirect, get_object_or_404

from clinic_users.decorators import role_required
from clinic_users.models import User
from notifications.models import Notification

from .models import FollowUp
from .forms import FollowUpForm
from patient_records.models import Patient


@role_required(['admin', 'follow_up'])
def follow_ups_list(request):
    follow_ups = FollowUp.objects.select_related(
        'patient'
    ).order_by(
        '-date'
    )

    return render(
        request,
        'follow_ups/follow_ups_list.html',
        {
            'follow_ups': follow_ups,
        }
    )


@role_required(['admin', 'follow_up'])
def create_follow_up(request, patient_id):
    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    if request.method == 'POST':
        form = FollowUpForm(request.POST)

        if form.is_valid():
            follow_up = form.save(commit=False)
            follow_up.patient = patient
            follow_up.save()

            if follow_up.status in ['review', 'needs_attention']:
                diet_doctors = User.objects.filter(
                    role='diet_doctor'
                )

                for doctor in diet_doctors:
                    Notification.objects.create(
                        recipient=doctor,
                        patient=patient,
                        title='Check-in Needs Review',
                        message=(
                            f'{patient.name} has a check-in marked as '
                            f'{follow_up.get_status_display()} on {follow_up.date}.'
                        ),
                        notification_type='follow_up'
                    )

            return redirect(
                'patient_detail',
                patient_id=patient.id
            )
    else:
        form = FollowUpForm()

    return render(
        request,
        'follow_ups/add_follow_up.html',
        {
            'form': form,
            'patient': patient,
        }
    )