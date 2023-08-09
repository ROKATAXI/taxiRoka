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


def send_activation_email(user):
    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login('ggom131@gmail.com', 'pusytktpalsmuyva')

        subject = 'Activate Your Account'
        message = f'Click the link to activate your account: http://127.0.0.1:8000/user/activate/{user.pk}/'
        sender_email = 'ggom131@gmail.com'
        recipient_email = user.email
        msg = f'Subject: {subject}\n\n{message}'
        smtp_server.sendmail(sender_email, recipient_email, msg)

    except smtplib.SMTPException as e:
        print("An error occurred:", str(e))
    finally:
        smtp_server.quit()

def activate_account(request, pk):
    User = get_user_model()

    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise Http404("User does not exist")

    # 계정을 활성화로 변경하거나 원하는 활성화 로직을 구현하세요
    user.is_active = True
    user.save()

    return render(request, 'user/account_activated.html')

def google_callback(request):
    print('2')
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
            return redirect('user:main')

        except CustomUser.DoesNotExist:
            return redirect('user:signup')
            
    
    except JSONDecodeError as e:
        return JsonResponse({'err_msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client

def send_email(request):
    return render(request, 'user/send_email.html')  # 이메일 전송 성공 시 보여줄 페이지





# kakao



def kakao_Auth_Redirect(request):
    code = request.GET.get('code',None)
    print(code)
    if code:
        print("code", code)
        #이제 토큰을 받아야함.
        headers = {
        'Content-type':'application/x-www-form-urlencoded;charset=utf-8'
        }
        content = {
        "grant_type": "authorization_code",
        "client_id": "7e2293a02b5609b94e47fc7bd7929328",
        "redirect_url": "http://127.0.0.1:8000/user/kakao/redirect",
        "code": code,
        }
        res = requests.post("https://kauth.kakao.com/oauth/token",headers=headers, data=content)
        print(res.status_code)
        if res.status_code == 200:
            print("성공")
            token_res = res.json()
            headers123 = {
                "Authorization" : "Bearer " + token_res['access_token'],
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            }
            res = requests.post("https://kapi.kakao.com/v2/user/me",headers=headers123)
            print("res2", res)
            if res.status_code == 200:
                profile_res = res.json()
                username = profile_res['properties']['nickname']
                id = profile_res['id']
                user = User.objects.filter(kakaoId=id)
                if user.first() is not None:
                    print("로그인")
                    login(request, user.first(), backend='django.contrib.auth.backends.ModelBackend')
                    return redirect("/")
                else:
                    print("새로 생성")
                    user = CustomUser()
                    user.username = username
                    user.kakaoId = id
                    user.save()
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            else:
                print("user정보 가져오기 실패")
        else:
            print("토근발급 실패")
    

    return redirect("/")


def kakao(request):
   return render(request, 'user/kakao.html')

