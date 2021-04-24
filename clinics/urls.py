from django.urls import path

from . import views

app_name = 'clinics'
urlpatterns = [
    path('search', views.clinics_search, name='search'),
    path('detail/<str:clinic_id>', views.clinics_detail, name='clinics_detail'),
    path('insert/<int:n_records>', views.clinics_bulk_insert, name='insert'),
    path('<int:clinic_id>/schedule/', views.clinic_schedule, name='clinic_schedule'),
    path('<int:sched_id>/schedule_appt/', views.schedule_appt, name='sched_appt'),
]
