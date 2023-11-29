from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .length import LengthRange

# 로그인 뷰는 auth_views.LoginView.as_view()를 사용하여 views.py에서 따로 지정할 필요 없음


def signup_view(request):

    context = {}

    # # 회원가입 요청
    # if request.method == "POST" :

    #     err_msg = ""

    #     # 세션에서 메세지 가져오고 세션에 저장된 내용 초기화
    #     if 'err_msg' in request.session :
    #         err_msg = request.session['err_msg']
    #         request.session['err_msg'] = ""

    #     # 입력 데이터 가져오기
    #     user_id = request.POST.get('user_id')
    #     user_pwd = request.POST.get('user_pwd')
    #     check_pwd = request.POST.get('check_pwd')
    #     user_name = request.POST.get('user_name')
    #     nickname = request.POST.get('nickname')
    #     email = request.POST.get('email')
    #     tel = request.POST.get('tel')

    #     # 각 데이터에 대한 양식 검사

    #     # 모든 데이터가 검사를 통과할 경우, 메인화면으로 리다이렉트

    #     # 하나 이상 실패한 경우, 회원가입 화면 페이지 반환

    #     context = {
    #         "user_id" : [user_id, ""],
    #         "user_pwd" : [user_pwd, ""],
    #         "check_pwd" : [check_pwd, ""],
    #         "user_name" : [user_name, ""],
    #         "nickname" : [nickname, ""],
    #         "email" : [email, ""],
    #         "tel" : [tel, ""],
    #         "err_msg" : err_msg,
    #     }

    #     return render(request, 'users/signup.html', context)

    # # 회원가입 페이지 접속
    # elif request.method == "GET" :

    #     err_msg = ""

    #     # 세션에서 메세지 가져오고 세션에 저장된 내용 초기화
    #     if 'err_msg' in request.session :
    #         err_msg = request.session['err_msg']
    #         request.session['err_msg'] = ""

    #     context = {
    #         "user_id" : ["", ""],
    #         "user_pwd" : ["", ""],
    #         "check_pwd" : ["", ""],
    #         "user_name" : ["", ""],
    #         "nickname" : ["", ""],
    #         "email" : ["", ""],
    #         "tel" : ["", ""],
    #         "err_msg" : err_msg,
    #     }

    return render(request, 'users/signup.html', context)


def my_page(request):
    if request.user.is_anonymous:
        return redirect('users:login_view')

    return render(request, 'users/my_page.html')


def update(request):

    user_info = User.objects.get(username=request.user.username)

    context = {
        'username': user_info.username,
        'email': user_info.email,
        'first_name': user_info.first_name,
        'last_name': user_info.last_name,
    }

    return render(request, 'users/update.html', context)


def change_pwd(request):
    if request.user.is_anonymous:
        return redirect('users:login_view')

    return render(request, 'users/change_pwd.html')
