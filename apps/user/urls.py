from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    # 구글 소셜로그인
    path('google/login', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
    path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
]
