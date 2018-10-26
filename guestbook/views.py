from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from guestbook.models import Guestbook


def list(request):
    messages = Guestbook.objects.all().order_by('-id')
    data = {'messages': messages}

    return render(request,"guestbook/list.html",data)


def add(request):
    authuser = request.session.get('authuser')
    guestbook = Guestbook()

    if authuser is None:
        guestbook.name = request.POST['name']
        guestbook.password = request.POST['password']
    else:
        guestbook.name = authuser['name']
        guestbook.password = authuser['password']

    guestbook.message = request.POST['content']
    guestbook.save()

    return HttpResponseRedirect("/guestbook/list")


def deleteform(request):
    id = request.GET['id']
    data = {'id':id}

    return render(request,"guestbook/deleteform.html",data)


def delete(request):
    id = request.POST['id']
    password = request.POST['password']
    comment = Guestbook.objects.filter(id=id, password=password)

    if len(comment)==0:
        return HttpResponseRedirect("/guestbook/deleteform?result=fail&id={}".format(id))

    comment.delete()
    return HttpResponseRedirect("/guestbook/list")







def ajax(request):
    return render(request, 'guestbook/ajax.html')


def api_list(request):
    p = request.GET['p']
    page = (int(p) - 1) * 5
    list_messages = []

    messages = Guestbook.objects.all().order_by('-id')[page:page+5]
    messages = messages.values()

    for a in messages:
        list_messages.append(a)

    data = {'messages':list_messages}
    return JsonResponse(data)









