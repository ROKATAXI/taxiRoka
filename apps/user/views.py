from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as authlogin
from django.contrib.auth.forms import UserChangeForm
from allauth.account.views import LoginView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import CustomUser
from apps.matching.models import MatchingRoom, Matching 
from apps.vacation.models import Vacation
from django.http import Http404
from django.contrib.auth.backends import ModelBackend
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
    if not request.user.location:
        return render(request, 'user/social.html')
    return redirect('matching:main') 

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

        subject = '[TaxiRoka] 본인 확인을 위한 이메일 인증을 완료해주세요!'
        activation_link = f'http://taxiroka.p-e.kr:8000/user/activate/{user.pk}/'
        
        sender_email = 'taxiroka2@gmail.com'
        recipient_email = user.email

        email_body = f'''
            <html>
                <body>
                    <h1>이메일 인증</h1>
                    <h3><br>서비스 이용을 위해 가입한 계정이 본인인지 확인하려고 합니다. <br>아래 버튼을 눌러 이메일 인증을 해주세요.<br></h3>
                    <a href="{activation_link}">
                        <button style="background-color: #007BFF; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
                            인증하기
                        </button>
                    </a>
                </body>
            </html>
        '''

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(email_body, 'html'))  # HTML message
        smtp_server.sendmail(sender_email, recipient_email, msg.as_string())

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
    print("함수호출횟수",code)
    if code:
        print("code", code)
        #이제 토큰을 받아야함.
        headers = {
        'Content-type':'application/x-www-form-urlencoded;charset=utf-8'
        }
        content = {
        "grant_type": "authorization_code",
        "client_id": "7e2293a02b5609b94e47fc7bd7929328",
        "redirect_url": "https://taxiroka.p-e.kr/user/kakao/redirect",
        # "redirect_url": "http://127.0.0.1:8000/user/kakao/redirect",
        "code": code,
        }
        res = requests.post("https://kauth.kakao.com/oauth/token",headers=headers, data=content)
        print(res)
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
                kakao_email = profile_res['kakao_account']['email']
                id = profile_res['id']
                user = User.objects.filter(kakaoId=id).first()
                print(id, username)
                if user is not None:
                    print(type(user))
                    print("로그인")
                    authlogin(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('user:social_login')
                else:
                    print("새로 생성")
                    user = User()
                    print(user)
                    user.username = kakao_email
                    print(user.username)
                    user.first_name = username
                    user.email = kakao_email
                    user.kakaoId = id
                    user.save()
                    authlogin(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('user:social_login')
            else:
                print("user정보 가져오기 실패")
        else:
            print("토근발급 실패")
    

    return redirect("/")

# 마이페이지
def mypage(request):
    matching_all = Matching.objects.filter(user_id = request.user).count()
    matching_ing = Matching.objects.filter(user_id = request.user, matching_room_id__end_yn = True).count()
    matching_end = Matching.objects.filter(user_id = request.user, matching_room_id__end_yn = False).count()
    vacations = Vacation.objects.filter(user_id = request.user)

    ctx= {
        "matching_all": matching_all,
        "matching_ing": matching_ing,
        "matching_end": matching_end,
        "vacations":vacations,
    }

    return render(request, 'user/mypage.html', context=ctx)

@login_required
def modify(request):
    user = request.user

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        phone = request.POST.get('phone')
        location = request.POST.get('location')

        user.first_name = first_name
        user.phone = phone
        user.location = location
        user.save()

        messages.success(request, '사용자 정보가 수정되었습니다.')
        return redirect('/')

    context = {
        'user': user,  # 수정된 사용자 정보를 넘겨줍니다.
    }

    return render(request, 'user/modify.html', context)
