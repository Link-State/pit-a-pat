from django.shortcuts import render, redirect

# Create your views here.
def createPaper(request) :

    if request.method == "POST" :
        user_id = request.session.get('user')
    
        # 세션 존재
        if user_id :
            pass

        # 세션 없음

    return render(request, 'papers/dummy1.html')

def loadPaper(request, paper_uid) :

    err_msg = ""

    # 세션에 저장된 오류 메세지 받아오기
    if 'err_msg' in request.session :
        err_msg = request.session['err_msg']
        request.session['err_msg'] = ""

    context = {"uid" : paper_uid, "err_msg" : err_msg}
    return render(request, 'papers/dummy2.html', context)
