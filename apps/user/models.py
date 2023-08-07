from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# ERD CLOUD 링크: https://www.erdcloud.com/d/zB3wiAaQY7PxnzLyY

class CustomUser(AbstractUser):
    # 아이디, 비밀번호, 이름, 전화번호, 이메일, 부대위치, 신고횟수, 가입일, 입대일, 전역일
    phone = models.CharField(max_length=11)
    location = models.CharField(max_length=10)
    count = models.IntegerField(default=0)
    join_date = models.DateTimeField(default=timezone.now)
    in_date = models.DateField(default=timezone.now)
    out_date = models.DateField(default=timezone.now)
    kakao_id = models.CharField(
        "Kakao Id", max_length=100, default=None, null=True, blank=True
    )
