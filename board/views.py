from django.db.models import Max, F
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from board.models import Board

# Create your views here.
from user.models import User


def list(request):
    pagenum = request.GET.get('page')
    pagenum = 1 if pagenum is None else int(pagenum)
    request.session['pagenum'] = pagenum
    authuser = request.session.get('authuser')

    contents = Board.objects.select_related().order_by('-group_no', 'order_no')
    #----------------------------검색 기능 구현-------------------------------
    keyword = request.GET.get('keyword',"")
    if keyword!="":
        contents = contents.filter(title__icontains=keyword)
    #------------------------------------------------------------------------
    length = len(contents)
    contentslen = (length // 5) + 1 if ((length / 5) > (length // 5)) else (length // 5)

    if pagenum == 1:
        contents = contents[:5]
    else:
        index = (pagenum-1) * 5
        contents = contents[index:(index+5)]

    data = {'contents':contents, 'authuser':authuser, 'len':contentslen,
            'pagenum':pagenum, 'boardlen':length, 'keyword':keyword }

    return render(request,'board/list.html', data)


def find(request):
    # ----------------------------검색 기능 구현-------------------------------
    keyword = request.POST.get('keyword')
    if keyword is None:
        return HttpResponseRedirect("/board/list")
    else:
        return HttpResponseRedirect("/board/list?keyword={}".format(keyword))
    # ------------------------------------------------------------------------


def modifyform(request):
    id = request.GET['id']
    content = Board.objects.get(id=id)
    data = {'content': content}
    print(id)

    return render(request,'board/modifyform.html',data)


def modify(request):
    pagenum = request.session['pagenum']
    id = request.GET['id']
    modifyboard = Board.objects.get(id=id)
    modifyboard.title = request.POST['title']
    modifyboard.content = request.POST['content']
    modifyboard.save()

    return HttpResponseRedirect("/board/view?page={0}&id={1}".format(pagenum,id))


def view(request):
    authuser = request.session.get('authuser')
    hitview = request.session.get('hitview')
    id = request.GET['id']
    content = Board.objects.all().filter(id=id)

    if authuser is not None:
    # 로그인이 되어 있을 때
        if hitview is None:
        # 조회수가 전부 0 일때(request.session['hitview']이 없음)
            request.session['hitview'] = {id : [authuser['id']]}
            content.update(hit=F('hit')+1)
        else:
        # request.session['hitview']이 존재 할 때
            if hitview.get(id) is None:
            # 특정 게시물을 처음 조회 할 때
                hitview[id] = [authuser['id']]
                request.session['hitview'] = hitview
                content.update(hit=F('hit') + 1)
            elif (authuser['id'] in hitview[id])==False:
            # 특정 유저가 특정 게시물을 처음 조회 했을 때
                hitview[id].append(authuser['id'])
                request.session['hitview'] = hitview
                content.update(hit=F('hit') + 1)
    else:
    # 로그인이 안 되어 있을 때
        content.update(hit=F('hit') + 1)

    data = {'content':content[0], 'authuser':authuser}

    return render(request,'board/view.html',data)


def writeform(request):
    id = request.GET.get('id')
    data = {'id':id}
    return render(request,'board/writeform.html',data)


def write(request):
    newboard = Board()
    newboard.userid_id = request.GET['userid']
    newboard.title = request.POST['title']
    newboard.content = request.POST['content']
    newboard.save()

    pagenum = request.session['pagenum']

    return HttpResponseRedirect("/board/list?page={}".format(pagenum))


def reply(request):
    boardid = request.GET['id']
    parent_board = Board.objects.get(id=boardid)
    newreply = Board()
    newreply.group_no = parent_board.group_no

    #group = Board.objects.all().filter(group_no=parent_board.group_no)


    if parent_board.order_no == 1:
    # 제일 윗 글에 답글 달 때
        max_order_no = Board.objects.filter(group_no=parent_board.group_no).aggregate(Max('order_no'))
        newreply.order_no = max_order_no['order_no__max'] + 1
        newreply.depth = 1
    else:
    # 답글이 여러개 일 때
        if parent_board.depth >= 1:
        # 답글에 답글이 없을 때
            oth_reply = Board.objects.all().filter(order_no__gt=parent_board.order_no)
            oth_reply.update(order_no=F('order_no') + 1)
            newreply.order_no = parent_board.order_no + 1
            newreply.depth = parent_board.depth + 1


    newreply.userid_id = request.GET['userid']
    newreply.title = request.POST['title']
    newreply.content = request.POST['content']
    newreply.save()

    pagenum = request.session['pagenum']

    return HttpResponseRedirect("/board/list?page={}".format(pagenum))


def deleteform(request):
    id = request.GET['id']
    authuser = request.session['authuser']
    deleteboard = Board.objects.get(id=id)
    if authuser['id'] != deleteboard.userid_id:
        return HttpResponseRedirect("/board/list")

    data = {'id':id}
    return render(request,'board/deleteform.html',data)


def delete(request):
    pagenum = request.session['pagenum']
    id = request.POST['id']
    password = request.POST['password']
    content = Board.objects.get(id=id)
    user = User.objects.get(id=content.userid_id)

    if user.password != password:
        return HttpResponseRedirect("/board/deleteform?result=fail&id={0}&page={1}".format(id,pagenum))

    content.delete()
    hitview = request.session['hitview']
    if hitview.get(id) is not None:
        del(hitview[id])
        request.session['hitview'] = hitview

    return HttpResponseRedirect("/board/list?page={}".format(pagenum))
