from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from . import views

app_name = "users"
urlpatterns = [
    path('login_view', auth_views.LoginView.as_view(template_name='users/login.html'), name='login_view'), #로그인 뷰
    path('signup_view', views.signup_view, name='signup_view'),  #회원가입 뷰
]
