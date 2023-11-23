from django.shortcuts import render
from papers.models import Rolling_paper

def main(request):

    paper = None
    paper_list = []

    # 본인의 롤링페이퍼를 보여주는 경우
    if request.user.is_anonymous :
        paper = Rolling_paper.objects.all().order_by("-paper_number").values()

    # 전체 롤링페이퍼 중, 마지막으로 만들어진 롤링페이퍼를 보여주는 경우
    else :
        paper = Rolling_paper.objects.filter(nickname=request.user.username).order_by("-paper_number").values()
    

    # 내림차순 정렬, 순서대로 9개 선택
    i = 0
    for dic in paper :
        if i == 9 : break
        paper_list.append(dic)
        i += 1
    
    context = {
        "papers" : paper_list,
    }

    return render(request, 'main/main.html', context)
