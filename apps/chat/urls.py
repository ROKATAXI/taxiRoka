from django.urls import path
from .views import *

urlpatterns = [
    path("<str:room_uuid>/", chat, name = "chat"),
]
