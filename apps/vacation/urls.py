from django.urls import path
from .views import *

urlpatterns = [
    path('', vacation_list),
    path('create/', create_vacation),
    path('delete/<int:pk>/', delete_vacation),
]
