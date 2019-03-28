# coding: utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import os
from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
# from django.contrib import auth
# from django.contrib.auth.decorators import login_required
from functools import wraps


# 说明：这个装饰器的作用，就是在每个视图函数被调用时，都验证下有没法有登录，
# 如果有过登录，则可以执行新的视图函数，
# 否则没有登录则自动跳转到登录页面。
def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        # if request.session.get('is_login')=='1':
        #     return f(request,*arg,**kwargs)
        # else:
        print 'checkcheckchekccheckchekc'
        return redirect('/toMain/')
    return inner


@check_login
def index(request):
    # students=Students.objects.all()  ## 说明，objects.all()返回的是二维表，即一个列表，里面包含多个元组
    # return render(request,'index.html',{"students_list":students})
    # username1=request.session.get('username')

    # user_id1=request.session.get('user_id')
    # 使用user_id去数据库中找到对应的user信息

    # userobj=User.objects.filter(id=user_id1)
    print 111111111
    # if userobj:
    #     return render(request,'index.html',{"user":userobj[0]})
    # else:
    #     return render(request,'index.html',{'user','匿名用户'})

def toMain(request):
    return render(request, "main.html")


def firstPage(request):
    return render(request, "firstPage.html")


def refresh(request):
    x = os.popen("curl -X POST http://127.0.0.1:9090/-/reload").read()
    return render(request, "firstPage.html", {'rs': x})
