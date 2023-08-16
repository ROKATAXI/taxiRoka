from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'), 
    path('google/callback/', views.google_callback, name='google_callback'),
    path('send_email/', views.send_email, name='send_email'),
    path('activate/<int:pk>/', views.activate_account, name='activate_account'),
    path('login/social/', views.social_login,name='social_login'),
    path('kakao/redirect/',views.kakao_Auth_Redirect,name="kakaoAuth"), # 카카오디벨로퍼스
    path('mypage/',views.mypage,name="mypage"),
    path('test/',views.test,name="test"),
]
