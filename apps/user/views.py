from django.shortcuts import render, redirect
from django.contrib import auth
from .models import CustomUser 
from django.contrib.auth.backends import ModelBackend
from django.views import View
import requests
from django.contrib.auth import get_user_model
User = get_user_model()


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