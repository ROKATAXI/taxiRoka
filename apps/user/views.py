from django.shortcuts import render,redirect
from django.contrib import auth

# Create your views here.
def login(request):
    print("login")
    if request.method == 'POST' :
        print("login post")

        id = request.POST['id']
        password = request.POST['password']

        user = auth.authenticate(request, id=id, password=password)

        if user is None :
            print('login fail')
            return redirect('/login')
        else :
            auth.login(request, user)
            user, _ = user.objects.get_or_create(user=user, name=user.username)
            return redirect('/')

    return render(request, 'user/login.html')