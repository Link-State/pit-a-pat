from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .length import LengthRange

# 로그인 뷰는 auth_views.LoginView.as_view()를 사용하여 views.py에서 따로 지정할 필요 없음


def signup_view(request):

    context = {}

    # 회원가입 요청
    if request.method == "POST" :

        # 입력 데이터 가져오기
        user_id = request.POST.get('user_id')
        user_pwd = request.POST.get('user_pwd')
        check_pwd = request.POST.get('check_pwd')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        context = {
            'user_id' : [user_id, ""],
            'user_pwd' : [user_pwd, ""],
            'check_pwd' : [check_pwd, ""],
            'first_name' : [first_name, ""],
            'last_name' : [last_name, ""],
            'email' : [email, ""],
        }

        # 아이디 길이 검사
        if len(user_id) < LengthRange.ID.MIN or len(user_id) > LengthRange.ID.MAX :
            context['user_id'][1] = "아이디는 최소 1자, 최대 150자까지만 사용할 수 있습니다."

        # 아이디 중복 검사
        user = User.objects.filter(username=user_id)
        if user.count() != 0 :
            context['user_id'][1] = "사용 불가능한 아이디입니다."
        
        # 비밀번호 길이 검사
        if len(user_pwd) < LengthRange.PassWord.MIN or len(user_pwd) > LengthRange.PassWord.MAX :
            context['user_pwd'][1] = "비밀번호는 최소 1자, 최대 128자까지만 사용할 수 있습니다."

        # 비밀번호 확인 길이 검사
        if len(check_pwd) < LengthRange.PassWord.MIN or len(check_pwd) > LengthRange.PassWord.MAX :
            context['check_pwd'][1] = "비밀번호는 최소 1자, 최대 128자까지만 사용할 수 있습니다."

        # 성 길이 검사
        if len(first_name) < LengthRange.FirstName.MIN or len(first_name) > LengthRange.FirstName.MAX :
            context['first_name'][1] = "성은 최소 1자, 최대 50자까지만 사용할 수 있습니다."

        # 이름 길이 검사
        if len(last_name) < LengthRange.LastName.MIN or len(last_name) > LengthRange.LastName.MAX :
            context['last_name'][1] = "이름은 최소 1자, 최대 50자까지만 사용할 수 있습니다."

        # 이메일 길이 검사
        if len(email) < LengthRange.Email.MIN or len(email) > LengthRange.Email.MAX :
            context['email'][1] = "이메일은 최소 1자, 최대 254자까지만 사용할 수 있습니다."

        # 비밀번호와 비밀번호 확인 검사
        if user_pwd != check_pwd :
            context['user_pwd'][1] = ""
            context['check_pwd'][1] = "비밀번호가 일치하지 않습니다."
        
        # 하나 이상 실패한 경우, 회원가입 화면 페이지 반환
        for key in context.keys() :
            if context[key][1] != "" :
                return render(request, 'users/signup.html', context)

        # 모든 데이터가 검사 통과, DB에 계정정보 추가
        user = User.objects.create_user(
            password=user_pwd,
            username=user_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        return redirect('users:login_view')

    # 회원가입 페이지 접속
    elif request.method == "GET" :
        render(request, 'users/signup.html')

    return render(request, 'users/signup.html', context)


def my_page(request):
    if request.user.is_anonymous:
        return redirect('users:login_view')
    
    context = {}

    return render(request, 'users/my_page.html')


def update(request):

    # user_info = User.objects.get(username=request.user.username)

    # context = {
    #     'username': user_info.username,
    #     'email': user_info.email,
    #     'first_name': user_info.first_name,
    #     'last_name': user_info.last_name,
    # }

    return render(request, 'users/update.html')


def change_pwd(request):
    if request.user.is_anonymous:
        return redirect('users:login_view')

    return render(request, 'users/change_pwd.html')

def check_id(request) :
    if request.method == "POST" :
        
        alert = "exist"

        # 입력 데이터 가져오기
        user_id = request.POST.get("user_id")
        
        # 아이디 검색
        user = User.objects.filter(username=user_id)

        # 아이디 양식이 맞지 않는 경우
        if len(user_id) < LengthRange.ID.MIN or len(user_id) > LengthRange.ID.MAX :
            alert = "wrong_form"
        # 존재하지 않는 경우,
        elif user.count() == 0 :
            alert = "non_exist"
        
    return HttpResponse(alert)
