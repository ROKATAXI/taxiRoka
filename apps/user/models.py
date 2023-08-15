from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# ERD CLOUD 링크: https://www.erdcloud.com/d/zB3wiAaQY7PxnzLyY

class Location(models.TextChoices):
    Sangmudae = 'Sangmudae', '상무대' 

class CustomUser(AbstractUser):
    # 아이디, 비밀번호, 이름, 전화번호, 이메일, 부대위치, 신고횟수, 가입일, 입대일, 전역일, 알림수
    phone = models.CharField(max_length=11)
    location = models.CharField(max_length=10, choices=Location.choices, default=Location.Sangmudae)
    count = models.IntegerField(default=0)
    join_date = models.DateTimeField(default=timezone.now)
    in_date = models.DateField(null=True,blank=True)
    out_date = models.DateField(null=True,blank=True)
    kakaoId = models.IntegerField(null=True,blank=True)