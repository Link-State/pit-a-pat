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
