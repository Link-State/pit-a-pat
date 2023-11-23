from django.shortcuts import render, redirect
from users.models import User
from papers.models import Rolling_paper
from .models import Message
from .length import LengthRange
from django.utils import timezone

# Create your views here.
def createMessage(request) :

    if request.method == "POST" :

        # 로그인 상태가 아닐 경우
        if request.user.is_anonymous :
            return redirect('users:login_view')
        
        # 로그인 상태일 경우
        paper_uid = request.POST.get('paper_uid')
        content = request.POST.get('content')

        paper = Rolling_paper.objects.filter(paper_number=paper_uid)

        # 해당 롤링페이퍼가 존재하지 않으면 메인으로 리다이렉트
        if paper.count() != 1 :
            return redirect('/papers/'+str(paper_uid))
        
        # 글자 수 양식이 맞지 않으면 롤링페이퍼 수정 페이지로 리다이렉트
        if len(content) < LengthRange.Content.MIN or len(content) > LengthRange.Content.MAX :

            request.session['err_msg'] = "글자수를 넘김"

            return redirect('/papers/'+str(paper_uid))

        # 메세지 DB에 데이터 추가
        user = User.objects.get(id=request.user.username)
        message = Message.objects.create(paper_number=paper_uid, content=content, wrote=timezone.now(), modified=timezone.now(), nickname=user)

        # 롤링페이퍼 DB에 users 컬럼을 1 증가
        paper = paper.first()
        paper.users += 1
        paper.save()

        return redirect('/papers/'+str(paper_uid))

    return redirect('main:main')

def editMessage(request) :

    if request.method == "POST" :
        # 로그인 상태가 아닐 경우

        # 로그인 상태일 경우

        pass

    return redirect('main:main')