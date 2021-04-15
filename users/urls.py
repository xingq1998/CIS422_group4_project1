from django.urls import path

from . import views

urlpatterns = [
    # ex: /users/
    path('', views.index, name='index'),
    # ex: /users/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /users/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /users/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
