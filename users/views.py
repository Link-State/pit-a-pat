from django.contrib import auth
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from papers.models import Rolling_paper
from message.models import Message
from django.shortcuts import render, redirect
from .length import LengthRange
from django.http import JsonResponse

# 로그인 뷰는 auth_views.LoginView.as_view()를 사용하여 views.py에서 따로 지정할 필요 없음


def signup_view(request):

    context = {}

    # 회원가입 요청
    if request.method == "POST":

        # 입력 데이터 가져오기
        user_id = request.POST.get('user_id')
        user_pwd = request.POST.get('user_pwd')
        check_pwd = request.POST.get('check_pwd')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        context = {
            'user_id': [user_id, ""],
            'user_pwd': [user_pwd, ""],
            'check_pwd': [check_pwd, ""],
            'first_name': [first_name, ""],
            'last_name': [last_name, ""],
            'email': [email, ""],
        }

        # 아이디 길이 검사
        if len(user_id) < LengthRange.ID.MIN or len(user_id) > LengthRange.ID.MAX:
            context['user_id'][1] = "최소 1자, 최대 150자까지만 사용할 수 있습니다."

        # 비밀번호 길이 검사
        if len(user_pwd) < LengthRange.PassWord.MIN or len(user_pwd) > LengthRange.PassWord.MAX:
            context['user_pwd'][1] = "최소 1자, 최대 128자까지만 사용할 수 있습니다."

        # 비밀번호 확인 길이 검사
        if len(check_pwd) < LengthRange.PassWord.MIN or len(check_pwd) > LengthRange.PassWord.MAX:
            context['check_pwd'][1] = "최소 1자, 최대 128자까지만 사용할 수 있습니다."

        # 성 길이 검사
        if len(first_name) < LengthRange.FirstName.MIN or len(first_name) > LengthRange.FirstName.MAX:
            context['first_name'][1] = "최소 1자, 최대 50자까지만 사용할 수 있습니다."

        # 이름 길이 검사
        if len(last_name) < LengthRange.LastName.MIN or len(last_name) > LengthRange.LastName.MAX:
            context['last_name'][1] = "최소 1자, 최대 50자까지만 사용할 수 있습니다."

        # 이메일 길이 검사
        if len(email) < LengthRange.Email.MIN or len(email) > LengthRange.Email.MAX:
            context['email'][1] = "최소 1자, 최대 254자까지만 사용할 수 있습니다."

        # 비밀번호와 비밀번호 확인 검사
        if user_pwd != check_pwd:
            context['user_pwd'][1] = ""
            context['check_pwd'][1] = "비밀번호가 일치하지 않습니다."

        # 하나 이상 실패한 경우, 회원가입 화면 페이지 반환
        for key in context.keys():
            if context[key][1] != "":
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
    elif request.method == "GET":
        render(request, 'users/signup.html')

    return render(request, 'users/signup.html', context)


def my_page(request):
    if request.user.is_anonymous:
        return redirect('users:login_view')

    my_paper_querySet = Rolling_paper.objects.filter(
        nickname=request.user.username).values("paper_number", "subject")
    my_papers = [dic for dic in my_paper_querySet]

    my_message_querySet = Message.objects.filter(
        nickname=request.user.username).values("paper_number", "content")
    my_messages = [dic for dic in my_message_querySet]

    context = {
        "my_papers": my_papers,
        "my_messages": my_messages,
    }

    return render(request, 'users/my_page.html', context)


def update(request):

    # 수정할 정보를 담을 context
    context = {

    }

    if request.method == "POST":
        # 회원정보 수정 요청

        # 로그인 상태가 아니므로 로그인 화면으로 이동
        if request.user.is_anonymous:
            return redirect("users:login_view")

        # 로그인 상태이므로 각 입력데이터 양식 검사
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # 각 필드 양식 검사
        if 1 > len(last_name) or 30 < len(last_name):
            context['last_name'] = [last_name, "성 길이는 1~30자 까지 허용됩니다."]
        if 1 > len(first_name) or 30 < len(first_name):
            context['first_name'] = [first_name, "이름 길이는 1~30자 까지 허용됩니다."]
        if 1 > len(email) or 30 < len(email):
            context['email'] = [email, "이메일 길이는 1~30자 까지 허용됩니다."]

        # 하나라도 오류가 있을 경우, 정보수정 페이지 이동
        if len(context) > 1:
            return render(request, 'users/update.html', context)

        # DB에 저장된 유저 정보 가져오기
        user_info = User.objects.get(username=request.user.username)

        # 정보 수정 후, 저장
        user_info.first_name = first_name
        user_info.last_name = last_name
        user_info.email = email
        user_info.save()

        return redirect('users:my_page')

    elif request.method == "GET":
        # 회원정보 홈페이지 접근

        session_user = {
            "username": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
        }

        return render(request, 'users/update.html', session_user)

    return render(request, 'users/update.html', context)


def change_pwd(request):
    if request.user.is_anonymous:
        return redirect('users:login_view')
    else:
        if request.method == "POST":
            user = request.user
            new_password = request.POST["pwd"]
            confirm_pwd = request.POST["check_pwd"]
            if new_password == confirm_pwd:
                user.set_password(raw_password=new_password)
                user.save()
                logout(request)
                return redirect('users:login_view')
    return render(request, 'users/change_pwd.html')


def check_id(request):

    if request.method == "POST":
        user_id = request.POST.get("user_id")

        try:
            _id = User.objects.get(username=user_id)

        except:
            _id = None

        if _id is None:
            msg = "non_exist"
        else:
            msg = "exist"

    context = {'msg': msg}

    return JsonResponse(context)


def withdraw_view(request):
    if request.method == "POST":
        username = User.objects.filter(username=request.user.username)
        username = username.first()
        username.delete()
        logout(request)
        return redirect('main:main')
    return render(request, 'users/withdraw_view.html')
