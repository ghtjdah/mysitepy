from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from user import models
from user.models import User


def joinform(request):
    return render(request,'user/joinform.html')


def join(request):
    user = User()

    user.name = request.POST['name']
    user.email = request.POST['email']
    user.password = request.POST['password']
    user.gender = request.POST['gender']
    #agreeProv = request.POST['agreeProv']

    data = {'name': user.name, 'email': user.email,
            'password': user.password, 'gender': user.gender}

    #models.insert(data)
    user.save()

    return HttpResponseRedirect("/user/joinsuccess")


def joinsuccess(request):
    return render(request,"user/joinsuccess.html")


def loginform(request):
    return render(request,"user/loginform.html")


def login(request):
    email = request.POST['email']
    password = request.POST['password']

    #filter로 사용하여 받아오는 방식
    # user = User.objects.filter(email=email,password=password)
    # if len(user)==0:
    #     return HttpResponseRedirect("/user/loginform?result=fail")

    try:
        authuser = User.objects.get(email=email,password=password)
    except User.DoesNotExist:
        return HttpResponseRedirect("/user/loginform?result=fail")

    request.session['authuser'] = model_to_dict(authuser)
    return HttpResponseRedirect('/')


def logout(request):
    del(request.session['authuser'])
    del(request.session['pagenum'])
    return HttpResponseRedirect('/')


def modifyform(request):
    authuser = request.session['authuser']
    data = {'user':authuser}
    return render(request, "user/modifyform.html",data)


def modify(request):
    authuser = request.session['authuser']
    userinfos = User.objects.all().filter(id=authuser['id'])
    userinfo = userinfos[0]
    userinfo.password = request.POST['password']
    userinfo.gender = request.POST['gender']
    userinfo.save()
    request.session['authuser'] = model_to_dict(userinfo)

    return HttpResponseRedirect('/')


def checkemail(request):
    results = User.objects.filter(email=request.GET['email'])
    result = {'result':len(results)==0}
    return JsonResponse(result)