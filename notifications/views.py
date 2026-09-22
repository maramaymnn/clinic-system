from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Notification


@login_required
def notifications_list(request):

    if request.user.role == 'client':

        notifications = Notification.objects.filter(
            patient__user=request.user,
            is_read=False,
        ).order_by('-created_at')

        template = 'notifications/client_notifications.html'

    else:

        notifications = Notification.objects.filter(
            Q(recipient=request.user) |
            Q(recipient__isnull=True),
            is_read=False,
        ).order_by('-created_at')

        template = 'notifications/notifications_list.html'

    return render(
        request,
        template,
        {'notifications': notifications}
    )


@login_required
def mark_notification_read(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id
    )

    if request.user.role == 'client':

        if notification.patient and notification.patient.user == request.user:
            notification.is_read = True
            notification.save(update_fields=['is_read'])

    else:

        if (
            notification.recipient is None
            or notification.recipient == request.user
        ):
            notification.is_read = True
            notification.save(update_fields=['is_read'])

    return redirect('notifications')