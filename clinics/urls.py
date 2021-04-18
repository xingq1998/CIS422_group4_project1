from django.urls import path

from . import views

app_name = 'clinics'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:state>', views.state, name='state')
]
