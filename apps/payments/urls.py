from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('main/', views.main, name='main'),
]
