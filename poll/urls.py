import pdb

from django.urls import path
from . import views
from django.contrib import admin

app_name = 'poll'

urlpatterns = [
    path('<int:survey_id>/', views.Detail.as_view(), name='detail_survey'),
    # path('/choice', views.choise_save, name='choise_save')
]