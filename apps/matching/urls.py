from django.urls import path
from . import views

app_name = 'matching'

urlpatterns = [
    path('', views.main, name = "main"),
    path('create/', views.matching_create, name="create"),
    path('apply/<int:pk>', views.matching_apply, name="apply"),
]
