from django.urls import path
from .views import *

urlpatterns = [
    path('', matching_list),
    path('create/', create_room),
]
