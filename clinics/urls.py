from django.urls import path

from . import views

app_name = 'clinics'
urlpatterns = [
    path('', views.index, name='index'),
    path('state/<str:state>', views.state, name='state'),
    path('search', views.clinics_search, name='search'),
    path('detail/<str:clinic_id>', views.clinics_detail, name='clinics_detail'),
]
