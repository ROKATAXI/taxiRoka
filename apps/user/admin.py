from django.contrib import admin
from .models import CustomUser

# 아래 코드에서 User를 CustomUser로 변경
admin.site.register(CustomUser)