from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm 
# from django.contrib.auth import 

# Create your views here.
def createMessage(request) :

    if request.method == "POST" :

        # 로그인이 아닐 경우,
        if True :
            return redirect('users:login_view')

        # 필수 필드 확인
        paper_uid = request.POST.get('paper_uid')
        content = request.POST.get('content')

        print(paper_uid, content)

        return redirect('main:main')

    return redirect('main:main')