from django.shortcuts import render, redirect
from django.contrib import auth
from .models import CustomUser 
from django.contrib.auth.backends import ModelBackend
import requests
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import View
import os

def main(request):
    return render(request, 'user/main.html')

def login(request):
    if request.method == 'POST':
        print("login post")
        user_id = request.POST['id']  
        password = request.POST['password']

        user = auth.authenticate(request, username=user_id, password=password)

        if user is None:
            print('login fail')
            return redirect('/')
            
        else:
            auth.login(request, user)
            user, _ = CustomUser.objects.get_or_create(user=user, name=user.username)
            return redirect('/')
    return render(request, 'user/login.html') 

def signup(request):   
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        location = request.POST['location']
        in_date = request.POST['in_date']
        out_date = request.POST['out_date']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        try:
            existing_user = CustomUser.objects.get(username=username)
            return redirect('/login/') 
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                first_name = first_name,
                last_name = last_name,
                password=password,
                phone=phone,
                location=location,
                in_date=in_date,
                out_date=out_date
            )
            user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'
            user.save()
            auth.login(request, user)
            return redirect('/')

    return render(request, 'user/signup.html')



# 카카오
# 참고 블로그 링크들:
# https://sangjuncha-dev.github.io/posts/framework/django/2021-10-11-django-oauth-kakao/
# https://doongjun.tistory.com/33
# https://velog.io/@yevini118/Django-allauth-%EC%B9%B4%EC%B9%B4%EC%98%A4-%EB%A1%9C%EA%B7%B8%EC%9D%B8%ED%95%98%EA%B8%B0



KAKAO_CONFIG = {
    "KAKAO_REST_API_KEY": "c283f8418bd3a80e54aaab718c5e3443",
    "KAKAO_REDIRECT_URI": "http://localhost:8000/kakao/callback/",
    "KAKAO_CLIENT_SECRET_KEY": "BmlcGQDxsjJJkRqrJ7VhZc5AtHMfGg06",
}

kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"



