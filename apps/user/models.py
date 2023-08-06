from django.db import models


# ERD CLOUD 링크: https://www.erdcloud.com/d/zB3wiAaQY7PxnzLyY

class User(models.Model):
    # 아이디, 비밀번호, 이름, 전화번호, 이메일, 부대위치, 신고횟수, 가입일, 입대일, 전역일
    user_id = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=30)
    location = models.CharField(max_length=10)
    count = models.IntegerField()
    join_date = models.DateTimeField()
    in_date = models.DateField()
    out_date = models.DateField()
