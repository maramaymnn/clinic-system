from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from patient_records.models import Patient
from subscriptions.models import Subscription
from diet_plans.models import DietPlan
from exercise_plans.models import ExercisePlan
from follow_ups.models import FollowUp
from progress.models import Progress
from appointments.models import Appointment
from notifications.models import Notification


def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'client':
            return redirect('client_dashboard')

        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.role == 'client':
                return redirect('client_dashboard')

            return redirect('dashboard')

        return render(
            request,
            'clinic_users/login.html',
            {
                'error': 'Invalid username or password.'
            }
        )

    return render(
        request,
        'clinic_users/login.html'
    )


def logout_view(request):
    logout(request)
    return redirect('login')


def get_client_patient(request):
    if not request.user.is_authenticated:
        return None

    if request.user.role != 'client':
        return None

    return Patient.objects.filter(
        user=request.user
    ).first()


@login_required
def client_dashboard(request):
    if request.user.role != 'client':
        return redirect('dashboard')

    patient = get_client_patient(request)

    if patient is None:
        return render(
            request,
            'clinic_users/client_dashboard.html',
            {
                'patient': None
            }
        )

    notifications = Notification.objects.filter(
        Q(recipient=request.user) |
        Q(recipient__isnull=True),
        is_read=False
    ).order_by('-created_at')

    subscriptions = Subscription.objects.filter(
        patient=patient
    ).order_by('-start_date')

    diet_plans = DietPlan.objects.filter(
        patient=patient
    ).prefetch_related(
        'meal_images'
    ).order_by('-start_date')

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
    ).select_related(
        'coach'
    ).order_by(
        '-date',
        '-start_time'
    )

    context = {
        'patient': patient,
        'subscriptions': subscriptions,
        'diet_plans': diet_plans,
        'exercise_plans': exercise_plans,
        'follow_ups': follow_ups,
        'progress_records': progress_records,
        'appointments': appointments,
        'notifications': notifications,
    }

    return render(
        request,
        'clinic_users/client_dashboard.html',
        context
    )


@login_required
def client_profile(request):
    if request.user.role != 'client':
        return redirect('dashboard')

    patient = get_client_patient(request)

    return render(
        request,
        'clinic_users/client_profile.html',
        {
            'patient': patient
        }
    )


@login_required
def client_membership(request):
    if request.user.role != 'client':
        return redirect('dashboard')

    patient = get_client_patient(request)

    if patient:
        subscriptions = Subscription.objects.filter(
            patient=patient
        ).order_by('-start_date')
    else:
        subscriptions = Subscription.objects.none()

    return render(
        request,
        'clinic_users/client_membership.html',
        {
            'patient': patient,
            'subscriptions': subscriptions
        }
    )


@login_required
def client_nutrition(request):
    if request.user.role != 'client':
        return redirect('dashboard')

    patient = get_client_patient(request)

    if patient:
        diet_plans = DietPlan.objects.filter(
            patient=patient
        ).prefetch_related(
            'meal_images'
        ).order_by('-start_date')
    else:
        diet_plans = DietPlan.objects.none()

    return render(
        request,
        'clinic_users/client_nutrition.html',
        {
            'patient': patient,
            'diet_plans': diet_plans
        }
    )


@login_required
def client_workout(request):
    if request.user.role != 'client':
        return redirect('dashboard')

    patient = get_client_patient(request)

    if patient:
        exercise_plans = ExercisePlan.objects.filter(
            patient=patient
        ).order_by('-start_date')
    else:
        exercise_plans = ExercisePlan.objects.none()

    return render(
        request,
        'clinic_users/client_workout.html',
        {
            'patient': patient,
            'exercise_plans': exercise_plans
        }
    )


@login_required
def client_progress(request):
    if request.user.role != 'client':
        return redirect('dashboard')

    patient = get_client_patient(request)

    if patient:
        progress_records = Progress.objects.filter(
            patient=patient
        ).order_by('-date')
    else:
        progress_records = Progress.objects.none()

    return render(
        request,
        'clinic_users/client_progress.html',
        {
            'patient': patient,
            'progress_records': progress_records
        }
    )


@login_required
def client_checkins(request):
    if request.user.role != 'client':
        return redirect('dashboard')

    patient = get_client_patient(request)

    if patient:
        follow_ups = FollowUp.objects.filter(
            patient=patient
        ).order_by('-date')
    else:
        follow_ups = FollowUp.objects.none()

    return render(
        request,
        'clinic_users/client_checkins.html',
        {
            'patient': patient,
            'follow_ups': follow_ups
        }
    )


@login_required
def client_bookings(request):
    if request.user.role != 'client':
        return redirect('dashboard')

    patient = get_client_patient(request)

    if patient:
        appointments = Appointment.objects.filter(
            patient=patient
        ).select_related(
            'coach'
        ).order_by(
            '-date',
            '-start_time'
        )
    else:
        appointments = Appointment.objects.none()

    return render(
        request,
        'clinic_users/client_bookings.html',
        {
            'patient': patient,
            'appointments': appointments
        }
    )
@login_required
def create_client_account(request, patient_id):
    if request.user.role not in ['admin', 'receptionist']:
        return redirect('dashboard')

    patient = Patient.objects.get(id=patient_id)

    if patient.user:
        return redirect('patient_detail', patient_id=patient.id)

    User = get_user_model()

    username = f"client_{patient.id}"

    if User.objects.filter(username=username).exists():
        return redirect('patient_detail', patient_id=patient.id)

    user = User.objects.create_user(
        username=username,
        password='test1234',
        role='client'
    )

    patient.user = user
    patient.is_online = True
    patient.save(update_fields=['user', 'is_online'])

    messages.success(request, "Client account created successfully.")

    return redirect('patient_detail', patient_id=patient.id)