from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .length import LengthRange

# 로그인 뷰는 auth_views.LoginView.as_view()를 사용하여 views.py에서 따로 지정할 필요 없음


def signup_view(request):

    context = {}
    msg = ""

    # 세션에서 메세지 가져오고 세션에 저장된 내용 초기화
    if 'msg' in request.session :
        msg = request.session['msg']
        request.session['msg'] = ""

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
            "msg" : msg,
        }

        # 아이디 길이 검사
        if len(user_id) < LengthRange.ID.MIN or len(user_id) > LengthRange.ID.MAX :
            context['user_id'] = [user_id, "아이디 길이가 너무 깁니다."]
    
        # 비밀번호 길이 검사
        if len(user_pwd) < LengthRange.PassWord.MIN or len(user_pwd) > LengthRange.PassWord.MAX :
            context['user_pwd'] = [user_pwd, "현재 비밀번호 길이가 너무 깁니다."]

        # 비밀번호 확인 길이 검사
        if len(check_pwd) < LengthRange.PassWord.MIN or len(check_pwd) > LengthRange.PassWord.MAX :
            context['check_pwd'] = [check_pwd, "바꾸려는 비밀번호 길이가 너무 깁니다."]

        # 성 길이 검사
        if len(first_name) < LengthRange.FirstName.MIN or len(first_name) > LengthRange.FirstName.MAX :
            context['first_name'] = [first_name, "성의 길이가 너무 깁니다."]

        # 이름 길이 검사
        if len(last_name) < LengthRange.LastName.MIN or len(last_name) > LengthRange.LastName.MAX :
            context['last_name'] = [last_name, "이름의 길이가 너무 깁니다."]

        # 이메일 길이 검사
        if len(email) < LengthRange.Email.MIN or len(email) > LengthRange.Email.MAX :
            context['email'] = [email, "이메일 길이가 너무 깁니다."]

        # 비밀번호와 비밀번호 확인 검사
        if user_pwd != check_pwd :
            context['user_pwd'] = [user_pwd, ""]
            context['check_pwd'] = [check_pwd, "비밀번호가 일치하지 않습니다."]
        
        # 하나 이상 실패한 경우, 회원가입 화면 페이지 반환
        if len(context) > 1 :
            return render(request, 'users/signup.html', context)

        # 모든 데이터가 검사를 통과할 경우,

        # DB에 계정정보 추가
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

        context = {
            "user_id" : ["", ""],
            "user_pwd" : ["", ""],
            "check_pwd" : ["", ""],
            "user_name" : ["", ""],
            "nickname" : ["", ""],
            "email" : ["", ""],
            "tel" : ["", ""],
            "msg" : msg,
        }

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
        
        user_id = request.POST.get("user_id")

        request.session['msg'] = "디폴트"

        # 양식 검사
        if len(user_id) < LengthRange.ID.MIN or len(user_id) > LengthRange.ID.MAX :
            request.session['msg'] = "1~150자 이내만 가능"
        
        user = User.objects.filter(username=user_id)

        # 이미 있음
        if user.count() != 0 :
            request.session['msg'] = "이미 사용중인 아이디 입니다."
        else :
            request.session['msg'] = "사용 가능한 아이디 입니다."
    
    return redirect('users:signup_view')
        
