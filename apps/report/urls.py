from django.urls import path
from .views import *

urlpatterns = [
    path("form/", show_report, name = "show_report"),
    path("", make_report, name = "make_report"),
]