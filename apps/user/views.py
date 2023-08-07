from django.shortcuts import render, redirect
from django.contrib import auth
from .models import CustomUser 
from django.contrib.auth.backends import ModelBackend

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
