from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse
from .models import CustomUser 
from json import JSONDecodeError
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.contrib.auth.backends import ModelBackend
from rest_framework import status
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google import views as google_view
from django.core.mail import send_mail
from django.http import JsonResponse
import requests
from json import JSONDecodeError
import smtplib
import os
import requests
from django.views import View
User = get_user_model()

def main(request):
    return render(request, 'user/main.html')

def login(request):
    if request.method == 'POST':
        user_id = request.POST['id']  
        password = request.POST['password']

        user = auth.authenticate(request, username=user_id, password=password)

        if user is None:
            print('login fail')
            return redirect(reverse('user:login'))
            
        else:
            print('login')
            auth.login(request, user)
            user = CustomUser.objects.get(username=user.username)
            return redirect('/')
    return render(request, 'user/login.html') 

def logout(request) :
    auth.logout(request)
    return redirect(reverse('user:main'))

def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    redirect_uri = GOOGLE_CALLBACK_URI
    print(2)
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}")


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
            user.is_active = False 
            user.save()

            send_activation_email(user)

            return redirect('user:send_email')

    return render(request, 'user/signup.html')
