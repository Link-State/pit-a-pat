from django.shortcuts import render, redirect
from django.contrib.auth.models import User as Auth_User
from papers.models import Rolling_paper
from message.models import Message
from .length import LengthRange

# Create your views here.
def createPaper(request) :

    if request.method == "POST" :

        # 로그인 상태가 아니면 로그인 화면으로 리다이렉트
        if request.user.is_anonymous :
            return redirect('users:login_view')
        
        # 로그인 상태인 경우
        user = Auth_User.objects.filter(username=request.user.username)

        # 해당 유저가 존재하지 않으면 메인화면으로 리다이렉트
        if user.count() != 1 :
            return redirect('main:main')

        # 롤링페이퍼 추가
        user = user.first()
        paper = Rolling_paper.objects.create(nickname=user)

        return redirect('/papers/'+str(paper.paper_number))

    return redirect('main:main')


def loadPaper(request, paper_uid) :

    err_msg = ""

    # 세션에 저장된 오류 메세지 받아오기
    if 'err_msg' in request.session :
        err_msg = request.session['err_msg']
        request.session['err_msg'] = ""

    paper = Rolling_paper.objects.filter(paper_number=paper_uid)

    # 존재하지 않는 페이지이면 메인화면으로 리다이렉트
    if paper.count() != 1 :
        return redirect('main:main')
    
    paper = paper.first()

    # 해당 롤링페이퍼의 메세지를 딕셔너리로 변환
    message_querySet = Message.objects.filter(paper_number=paper_uid).values("message_number", "nickname", "content", "modified")
    messages = [ dic for dic in message_querySet ]

    context = {
        "paper_number" : paper_uid,
        "subject" : paper.subject,
        "owner" : paper.nickname.username,
        "wrote" : paper.completed,
        "messages" : messages,
        "err_msg" : err_msg,
    }

    # 추후 롤링페이퍼 html 템플릿으로 변경
    return render(request, 'papers/dummy1.html', context)


def editPaper(request, paper_uid) :
    
    if request.method == "POST" :

        # 로그인 상태가 아니면 로그인 화면 리다이렉트
        if request.user.is_anonymous :
            return redirect('users:login_view')
        
        # 로그인 상태인 경우
        subject = request.POST.get('subject') # 찾을 수 없으면 None 반환

        paper = Rolling_paper.objects.filter(paper_number=paper_uid)

        # 해당 롤링페이퍼가 존재하지 않으면 메인 화면으로 리다이렉트
        if paper.count() != 1 :
            return redirect('main:main')
        
        paper = paper.first()
        
        # 롤링페이퍼 소유주가 아니면 롤링페이퍼 화면으로 리다이렉트
        if request.user.username != paper.nickname.username :
            request.session['err_msg'] = "권한이 없습니다."
            return redirect('/papers/'+str(paper_uid))

        # 롤링페이퍼 제목 양식 검사
        if len(subject) < LengthRange.Subject.MIN or len(subject) > LengthRange.Subject.MAX :
            request.session['err_msg'] = "제목은 최소 1자, 최대 50자까지 작성할 수 있습니다."
            return redirect('/papers/'+str(paper_uid))
        
        # 롤링페이퍼 DB 제목 수정
        paper.subject = subject
        paper.save()

        return redirect('/papers/'+str(paper_uid))

    return redirect('main:main')


def deletePaper(request, paper_uid) :

    if request.method == "POST" :

        # 로그인 상태가 아니면 로그인 화면으로 리다이렉트
        if request.user.is_anonymous :
            return redirect('users:login_view')

        # 로그인 상태인 경우
        paper = Rolling_paper.objects.filter(paper_number=paper_uid)

        # 롤링페이퍼가 존재하지 않으면 메인화면으로 리다이렉트
        if paper.count() != 1 :
            return redirect('main:main')
        
        paper = paper.first()

        # 롤링페이퍼 소유자가 본인이 아니면 롤링페이퍼 화면으로 리다이렉트
        if request.user.username != paper.nickname.username :
            request.session['err_msg'] = "권한이 없습니다."
            return redirect('/papers/'+str(paper_uid))
        
        # 롤링페이퍼 DB에서 삭제
        paper.delete()

        return redirect('main:main')

    return redirect('main:main')
