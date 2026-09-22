from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from patient_records.models import Patient
from follow_ups.models import FollowUp
from appointments.models import Appointment
from subscriptions.models import Subscription
from diet_plans.models import DietPlan
from exercise_plans.models import ExercisePlan
from progress.models import Progress
from notifications.models import Notification


@login_required(login_url='/login/')
def dashboard(request):

    role = request.user.role

    active_patients = Patient.objects.filter(
        status='active'
    ).count()

    follow_ups_today = FollowUp.objects.filter(
        date=date.today()
    ).count()

    appointments_today = Appointment.objects.filter(
        date=date.today()
    ).count()

    expiring_subscriptions = Subscription.objects.filter(
        end_date__range=[
            date.today(),
            date.today() + timedelta(days=7)
        ],
        status='active'
    ).count()

    context = {
        'active_patients': active_patients,
        'follow_ups_today': follow_ups_today,
        'appointments_today': appointments_today,
        'expiring_subscriptions': expiring_subscriptions,
    }

    for subscription in Subscription.objects.filter(
        end_date__range=[
            date.today(),
            date.today() + timedelta(days=7)
        ],
        status='active'
    ):
        already_notified = Notification.objects.filter(
            patient=subscription.patient,
            notification_type='subscription_expiry',
            is_read=False,
            message__contains=str(subscription.end_date)
        ).exists()

        if not already_notified:
            Notification.objects.create(
                patient=subscription.patient,
                title='Membership Expiring Soon',
                message=f'{subscription.patient.name} membership expires on {subscription.end_date}.',
                notification_type='subscription_expiry'
            )

    # NOTE: every branch below now also fires for 'admin', so an
    # admin sees the same role cards as everyone else, on top of the
    # receptionist cards. Previously only 'diet_doctor' etc. (without
    # 'admin') triggered these, so an admin only ever saw the first
    # "Active Clients" card.
    if role in ('diet_doctor', 'admin'):
        context.update({
            'diet_plans_count': DietPlan.objects.count(),
            'progress_count': Progress.objects.count(),
        })

    if role in ('exercise_coach', 'admin'):
        context.update({
            'exercise_plans_count': ExercisePlan.objects.count(),
            'appointments_today': appointments_today,
        })

    if role in ('follow_up', 'admin'):
        context.update({
            'follow_ups_today': follow_ups_today,
        })

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )