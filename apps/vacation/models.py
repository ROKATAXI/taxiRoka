from django.db import models

# Create your models here.
from apps.user.models import User
from apps.matching.models import *



class MatchingRoom(models.Model):
    # 휴가출발일, 휴가복귀일, 몇 번쨰 휴가인지,
    vacation_departure_date = models.DateField()
    vacation_return_date = models.DateField()
