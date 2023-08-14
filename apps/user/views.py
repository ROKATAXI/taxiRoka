from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as authlogin
from allauth.account.views import LoginView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import CustomUser 
from django.http import Http404
from django.contrib.auth.backends import ModelBackend
import requests
import smtplib
import os

User = get_user_model()

def main(request):
    return render(request, 'user/main.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']  
        password = request.POST['password']

        user = auth.authenticate(request, username=email, password=password)

        if user is None:
            messages.error(request, '이메일 또는 비밀번호가 올바르지 않습니다.')
            return redirect(reverse('user:login'))
            
        else:
            print('login')
            auth.login(request, user)
            user = CustomUser.objects.get(username=user.username)
            return redirect('matching:main')
    return render(request, 'user/login.html') 

@login_required
def google_callback(request):
    user = request.user
    if not user.location:  # location이 비어있다면
        # 추가 정보 입력 페이지로 이동
        return redirect('user:social_login')
    else:
        # 메인 페이지로 이동
        return redirect('matching:main')

def social_login(request):   
    if request.method == 'POST':
        user = request.user  # 현재 로그인한 유저 정보
        # 만약 user의 location이 비어있으면
        if not user.location:
            name = request.POST['first_name']
            phone = request.POST['phone']
            location = request.POST['location']

            # 업데이트
            user.first_name = name
            user.last_name = ''
            user.username = user.email  # email 업데이트
            user.phone = phone  # phone 업데이트
            user.location = location  # location 업데이트
            user.save()
        return redirect('matching:main')  # 메인 페이지로 리디렉트

    return render(request, 'user/social.html')

def logout(request) :
    auth.logout(request)
    return redirect(reverse('user:main'))

def signup(request):   
    if request.method == 'POST':
        first_name = request.POST['first_name'] 
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        location = request.POST['location']
       
        hashed_password = make_password(password)

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'username': email,
                'password': hashed_password,
                'phone': phone,
                'location': location,
                'is_active': False,
            }
        )

        if not created:
            messages.error(request, '중복된 이메일입니다.')
            return redirect(reverse('user:signup'))

        if created:
    # 새로운 객체가 생성된 경우
            user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'
            user.save()
            send_activation_email(user)
            return redirect('user:send_email')
        else:
    # 이미 객체가 존재하는 경우
            return render(request, 'user/signup.html', {'error_message': '이미 해당 이메일로 가입된 유저가 있습니다.'})

    return render(request, 'user/signup.html')


def send_activation_email(user):
    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login('taxiroka2@gmail.com', 'dwupjxznhziubjxl')

        subject = 'Activate Your Account'
        message = f'Click the link to activate your account: http://127.0.0.1:8000/user/activate/{user.pk}/'
        sender_email = 'taxiroka2@gmail.com'
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

    user.is_active = True
    user.save()

    return render(request, 'user/account_activated.html')


def send_email(request):
    return render(request, 'user/send_email.html')  


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
                user = User.objects.filter(kakaoId=id).first()
                print(id, username)
                if user is not None:
                    print("로그인")
                    authlogin(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect("/matching/")
                else:
                    print("새로 생성")
                    user = User()
                    print(user)
                    user.username = f"{id}@kakao.com"
                    print(user.username)
                    user.first_name = username
                    user.kakaoId = id
                    user.save()
                    authlogin(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('user:social_login')
            else:
                print("user정보 가져오기 실패")
        else:
            print("토근발급 실패")
    

    return redirect("/")


def mypage(request):
    return render(request, 'user/mypage.html')




