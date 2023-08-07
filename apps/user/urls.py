from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('', views.kakao, name='kakao'),
    path('main/', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    
    path('kakao/redirect/',views.kakao_Auth_Redirect,name="kakaoAuth")
]
