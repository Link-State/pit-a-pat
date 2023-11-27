from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as Auth_User
from django.shortcuts import render, redirect
from .length import LengthRange

# 로그인 뷰는 auth_views.LoginView.as_view()를 사용하여 views.py에서 따로 지정할 필요 없음

def signup_view(request):
    context = {}

    if request.method == "POST":

        err_msg = ""

        if 'err_msg' in request.session:
            err_msg = request.session['err_msg']
            request.session['err.msg'] = ""

        user_id = request.POST.get('user_id')
        user_pwd = request.POST.get('user_pwd')
        check_pwd = request.POST.get('check_pwd')
        user_name = request.POST.get('user_name')
        nickname = request.POST.get('nickname')
        email = request.POST.get('email')
        tel = request.POST.get('tel')

        context = {
                "user_id": [user_id, ""],
                "user_pwd": [user_pwd, ""],
                "check_pwd": [check_pwd, ""],
                "user_name": [user_name, ""],
                "nickname": [nickname, ""],
                "email:": [email, ""],
                "tel": [tel, ""],
            }
        
        i = 0
        
        # 닉네임 중복 검사
        temp = Auth_User.objects.filter(username=nickname)
        temp = temp.first()
    
        if temp.count() != 0 :
            context["user_name"][1] = "이미 있는 닉네임 어쩌구"
            i += 1

        # 양식 검사
        if len(user_id) > 30:
            context["user_id"][1] = "id에 오류생김"
            i += 1
        
        if len(user_pwd) > 30:
            context["user_pwd"][1] = "pwd에 오류생김"
            i += 1
        
        if check_pwd != user_pwd:
            context["check_pwd"][1] = "pwd와 check_pwd가 동일하지 않음"
            i += 1
        
        if len(user_name) > 30:
            context["user_name"][1] = "user_name가 너무 긺"
            i += 1
        
        if len(nickname) > 30:
            context["nickname"][1] = "nickname가 너무 긺"
            i += 1
        
        if len(email) > 30:
            context["email"][1] = "email이 너무 긺"
            i += 1
        
        if len(tel) > 30:
            context["tel"][1] = "tel이 너무 긺"
            i += 1

        # 오류가 하나라도 있었으면,
        if i != 0 :
            return render(request, 'users/signup.html', context)
    
        # 오류가 하나도 없었으면, DB에 저장
        Auth_User.objects.create(password=user_pwd, user_name=nickname)
        return redirect('users/login.html', context)
    elif request.method == "GET" :
        return render(request, 'users/signup.html')

