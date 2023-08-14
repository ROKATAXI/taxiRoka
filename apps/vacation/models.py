from django.db import models
from apps.user.models import CustomUser

class Vacation(models.Model):
    # 출발일, 복귀일, 도착지, user정보
    departure_date = models.DateField()
    arrival_date = models.DateField()

    departure_area = models.CharField(max_length=10)
    destination_area = models.CharField(max_length=10)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
