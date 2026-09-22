from django.shortcuts import render, redirect, get_object_or_404

from clinic_users.decorators import role_required

from .models import Subscription
from .forms import SubscriptionForm
from patient_records.models import Patient


@role_required(['admin', 'receptionist'])
def create_subscription(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    if request.method == 'POST':

        form = SubscriptionForm(request.POST)

        if form.is_valid():

            subscription = form.save(commit=False)
            subscription.patient = patient
            subscription.save()

            return redirect(
                'patient_detail',
                patient_id=patient.id
            )

    else:

        form = SubscriptionForm()

    return render(
        request,
        'subscriptions/add_subscription.html',
        {
            'form': form,
            'patient': patient,
        }
    )
@role_required(['admin', 'receptionist'])
def subscriptions_list(request):

    subscriptions = Subscription.objects.select_related(
        'patient'
    ).order_by(
        '-start_date'
    )

    return render(
        request,
        'subscriptions/subscriptions_list.html',
        {
            'subscriptions': subscriptions,
        }
    )
