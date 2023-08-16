from django.urls import path
from . import views

app_name = 'matching'

urlpatterns = [

    path('', views.main, name = "main"),
    path('create/', views.matching_create, name="create"),
    path('apply/room/<int:pk>', views.matching_apply, name="apply"),
    path('update/room/<int:pk>', views.matching_update, name="update"),
    path('delete/room/<int:pk>', views.matching_delete, name="delete"),
    path('history/', views.matching_history, name="history"),
    path('alarm-delete/<int:alarm_id>/', views.alarm_delete, name="alarm-delete"),
    path('questions/', views.questions, name="questions"),
]
