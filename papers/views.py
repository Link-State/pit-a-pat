from django.shortcuts import render, redirect
from django.contrib.auth.models import User as Auth_User
from papers.models import Rolling_paper
from message.models import Message

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
        paper = Rolling_paper.objects.create(subject="", nickname=user)

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
        "isOwner" : paper.nickname.username,
        "wrote" : paper.completed,
        "messages" : messages,
        "err_msg" : err_msg,
    }

    return render(request, 'papers/dummy1.html', context)
