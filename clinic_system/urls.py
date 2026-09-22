from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from dashboard.views import dashboard

from patient_records.views import (
patients,
create_patient,
patient_detail,
create_assessment,
)

from subscriptions.views import (
create_subscription,
subscriptions_list,
)

from diet_plans.views import create_diet_plan
from exercise_plans.views import create_exercise_plan

from follow_ups.views import (
create_follow_up,
follow_ups_list,
)

from progress.views import (
create_progress,
progress_list,
)

from clinic_users.views import (
login_view,
logout_view,
client_dashboard,
client_profile,
client_membership,
client_nutrition,
client_workout,
client_progress,
client_checkins,
client_bookings,
create_client_account,
)

from appointments.views import (
create_appointment,
appointments_list,
update_appointment_status,
)

from notifications.views import (
notifications_list,
mark_notification_read,
)

urlpatterns = [

path(
    'admin/',
    admin.site.urls
),

path(
    '',
    dashboard,
    name='dashboard'
),

path(
    'login/',
    login_view,
    name='login'
),

path(
    'logout/',
    logout_view,
    name='logout'
),

# =========================
# CLIENT PORTAL
# =========================

path(
    'client/',
    client_dashboard,
    name='client_dashboard'
),

path(
    'client/profile/',
    client_profile,
    name='client_profile'
),

path(
    'client/membership/',
    client_membership,
    name='client_membership'
),

path(
    'client/nutrition/',
    client_nutrition,
    name='client_nutrition'
),

path(
    'client/workout/',
    client_workout,
    name='client_workout'
),

path(
    'client/progress/',
    client_progress,
    name='client_progress'
),

path(
    'client/checkins/',
    client_checkins,
    name='client_checkins'
),

path(
    'client/bookings/',
    client_bookings,
    name='client_bookings'
),

# =========================
# PATIENTS
# =========================

path(
    'patients/',
    patients,
    name='patients'
),

path(
    'patients/add/',
    create_patient,
    name='create_patient'
),

path(
    'patients/<int:patient_id>/',
    patient_detail,
    name='patient_detail'
),
path(
    'patients/<int:patient_id>/create-account/',
    create_client_account,
    name='create_client_account'
),

# =========================
# SUBSCRIPTIONS
# =========================

path(
    'patients/<int:patient_id>/subscriptions/add/',
    create_subscription,
    name='create_subscription'
),

path(
    'subscriptions/',
    subscriptions_list,
    name='subscriptions'
),

# =========================
# DIET PLANS
# =========================

path(
    'patients/<int:patient_id>/diet-plans/add/',
    create_diet_plan,
    name='create_diet_plan'
),

# =========================
# EXERCISE PLANS
# =========================

path(
    'patients/<int:patient_id>/exercise-plans/add/',
    create_exercise_plan,
    name='create_exercise_plan'
),

# =========================
# FOLLOW-UPS
# =========================

path(
    'patients/<int:patient_id>/follow-ups/add/',
    create_follow_up,
    name='create_follow_up'
),

path(
    'follow-ups/',
    follow_ups_list,
    name='follow_ups'
),

# =========================
# PROGRESS / INBODY
# =========================

path(
    'patients/<int:patient_id>/progress/add/',
    create_progress,
    name='create_progress'
),

path(
    'progress/',
    progress_list,
    name='progress'
),

# =========================
# INITIAL ASSESSMENT
# =========================

path(
    'patients/<int:patient_id>/assessments/add/',
    create_assessment,
    name='create_assessment'
),

# =========================
# APPOINTMENTS
# =========================

path(
    'patients/<int:patient_id>/appointments/add/',
    create_appointment,
    name='create_appointment'
),

path(
    'appointments/',
    appointments_list,
    name='appointments'
),

path(
    'appointments/<int:appointment_id>/update-status/',
    update_appointment_status,
    name='update_appointment_status'
),

# =========================
# NOTIFICATIONS
# =========================

path(
    'notifications/',
    notifications_list,
    name='notifications'
),

path(
    'notifications/mark-read/<int:notification_id>/',
    mark_notification_read,
    name='mark_notification_read'
),
]

urlpatterns += static(
settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT
)