from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# 로그인 뷰는 auth_views.LoginView.as_view()를 사용하여 views.py에서 따로 지정할 필요 없음

def signup_view(request):
    
    return render(request, 'users/signup.html')