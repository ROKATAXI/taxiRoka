from django.shortcuts import render, redirect
from django.contrib import auth
from .models import CustomUser 
from json import JSONDecodeError
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.backends import ModelBackend
from rest_framework import status
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google import views as google_view
import os
import requests

# 구글 소셜로그인 변수 설정
state = os.environ.get("STATE")
BASE_URL = 'http://localhost:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'api/user/google/callback/'

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
            user = CustomUser.objects.get(username=user.username)
            return redirect('/')
    return render(request, 'user/login.html') 

def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

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

from django.http import JsonResponse
import requests
from json import JSONDecodeError

def google_callback(request):
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get('code')

    token_req = requests.post(f"https://oauth2.googleapis.com/token", data={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": GOOGLE_CALLBACK_URI,
    })
    
    try:
        token_req_json = token_req.json()
        error = token_req_json.get("error")

        if error is not None:
            raise JSONDecodeError(error)

        access_token = token_req_json.get('access_token')

        email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo", params={
            "access_token": access_token
        })
        email_req_status = email_req.status_code

        if email_req_status != 200:
            return JsonResponse({'err_msg': 'failed to get email'}, status=email_req_status)
        
        email_req_json = email_req.json()
        email = email_req_json.get('email')

        try:
            user = CustomUser.objects.get(email=email)
            auth.login(request, user)
            return HttpResponseRedirect(f"{BASE_URL}user/main/")

        except CustomUser.DoesNotExist:
            return HttpResponseRedirect(f"{BASE_URL}user/signup/?email={email}")
            
    
    except JSONDecodeError as e:
        return JsonResponse({'err_msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client