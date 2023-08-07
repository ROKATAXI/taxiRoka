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
            user, _ = CustomUser.objects.get_or_create(user=user, name=user.username)
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

    # 1. 받은 코드로 구글에 access token 요청
    token_req = requests.post(f"https://oauth2.googleapis.com/token", data={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": GOOGLE_CALLBACK_URI,
    })
    
    try:
        # 1-1. json으로 변환 & 에러 부분 파싱
        token_req_json = token_req.json()
        error = token_req_json.get("error")

        # 1-2. 에러 발생 시 종료
        if error is not None:
            raise JSONDecodeError(error)

        # 1-3. 성공 시 access_token 가져오기
        access_token = token_req_json.get('access_token')

        #################################################################

        # 2. 가져온 access_token으로 이메일값을 구글에 요청
        email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo", params={
            "access_token": access_token
        })
        email_req_status = email_req.status_code

        ### 2-1. 에러 발생 시 400 에러 반환
        if email_req_status != 200:
            return JsonResponse({'err_msg': 'failed to get email'}, status=email_req_status)
        
        ### 2-2. 성공 시 이메일 가져오기
        email_req_json = email_req.json()
        email = email_req_json.get('email')

        # return JsonResponse({'access': access_token, 'email': email})

        #################################################################

        # 3. 전달받은 이메일, access_token, code를 바탕으로 회원가입/로그인
        try:
            # 전달받은 이메일로 등록된 유저가 있는지 탐색
            user = CustomUser.objects.get(email=email)

            # FK로 연결되어 있는 socialaccount 테이블에서 해당 이메일의 유저가 있는지 확인
            social_user = SocialAccount.objects.get(user=user)

            # 있는데 구글계정이 아니어도 에러
            if social_user.provider != 'google':
                return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

            # 이미 Google로 제대로 가입된 유저 => 로그인 & 해당 우저의 jwt 발급
            data = {'access_token': access_token, 'code': code}
            accept = requests.post(f"{BASE_URL}api/user/google/login/finish/", data=data)
            accept_status = accept.status_code

            # 뭔가 중간에 문제가 생기면 에러
            if accept_status != 200:
                return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

            accept_json = accept.json()
            accept_json.pop('user', None)
            return JsonResponse(accept_json)

        except CustomUser.DoesNotExist:
    # 전달받은 이메일로 기존에 가입된 유저가 아예 없으면 => 새로 회원가입 페이지로 이동
            return HttpResponseRedirect(f"{BASE_URL}user/signup/?email={email}")
            
    
    except JSONDecodeError as e:
        # JSONDecodeError 발생 시 에러 처리
        return JsonResponse({'err_msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client