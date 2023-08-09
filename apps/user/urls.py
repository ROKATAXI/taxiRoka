from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('send_email/', views.send_email, name='send_email'),
    path('activate/<int:pk>/', views.activate_account, name='activate_account'),
    # 구글 소셜로그인
    path('google/login', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
]
