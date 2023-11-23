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
        paper_uid = request.POST.get('paper_uid') # 없을 경우 None 반환
        content = request.POST.get('content') # 없을 경우 None 반환

        paper = Rolling_paper.objects.filter(paper_number=paper_uid)

        # 해당 롤링페이퍼가 존재하지 않으면 메인으로 리다이렉트
        if paper.count() != 1 :
            return redirect('main:main')
        
        # 글자 수 양식이 맞지 않으면 롤링페이퍼 수정 페이지로 리다이렉트
        if len(content) < LengthRange.Content.MIN or len(content) > LengthRange.Content.MAX :
            request.session['err_msg'] = "글자수를 넘김"
            return redirect('/papers/'+str(paper_uid))

        # 메세지 DB에 데이터 추가
        user = User.objects.get(id=request.user.username)
        message = Message.objects.create(paper_number=paper_uid, content=content, nickname=user)

        # 롤링페이퍼 DB에 users 컬럼을 1 증가
        paper = paper.first()
        paper.users += 1
        paper.save()

        return redirect('/papers/'+str(paper_uid))

    return redirect('main:main')

def editMessage(request, message_uid) :

    if request.method == "POST" :

        # 로그인 상태가 아닐 경우
        if request.user.is_anonymous :
            return redirect('users:login_view')

        # 로그인 상태일 경우
        content = request.POST.get('content') # 없을 경우 None 반환

        message = Message.objects.filter(message_number=message_uid)

        # 메세지가 존재하지 않으면 메인으로 리다이렉트
        if message.count() != 1 :
            return redirect('main:main')
        
        message = message.first()
        paper = Rolling_paper.objects.get(paper_number=message.paper_number)
        
        # 글자 수 양식이 맞지 않으면 롤링페이퍼 수정 페이지로 리다이렉트
        if len(content) < LengthRange.Content.MIN or len(content) > LengthRange.Content.MAX :
            request.session['err_msg'] = "글자수를 넘김"
            return redirect('/papers/'+str(paper.paper_number))
        
        # 롤링페이퍼 소유자가 아니고 본인이 작성한 메세지가 아니면 롤링페이퍼 수정 페이지로 리다이렉트
        if request.user.username != paper.nickname and request.user.username != message.nickname :
            request.session['err_msg'] = "본인이 작성한 메세지만 삭제할 수 있습니다."
            return redirect('/papers/'+str(paper.paper_number))
        
        # 메세지 DB 수정 후 저장
        message.content = content
        message.modified = timezone.now()
        message.save()

        return redirect('/papers/'+str(paper.paper_number))

    return redirect('main:main')