# coding: utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import os
from django.shortcuts import render, redirect, HttpResponse
from forms import Forms
from userconfig.models import PrometheusUser
import hashlib


def tologin(request):
    return render(request, "login.html")


def toMain(request):
    return render(request, "main.html", {'user': request.session.get('userName')})


def firstPage(request):
    return render(request, "firstPage.html")


def refresh(request):
    x = os.popen("curl -X POST http://127.0.0.1:9090/-/reload").read()
    return render(request, "firstPage.html", {'rs': x})


def checklogin(request):
    if request.method == 'POST':
        try:
            f = Forms(request.POST)
            if f.is_valid():
                print(f.cleaned_data)
                username = f.cleaned_data['username']
                password = f.cleaned_data['password']
                md = hashlib.md5()
                md.update(password)
                password = md.hexdigest()
                pu = PrometheusUser.objects.filter(name=username, passwd=password)
                if len(pu) > 0:
                    request.session['userName'] = username
                    return render(request, "main.html", {'user': request.session.get('userName')})
                else:
                    return render(request, "login.html", {'error': u'用户名密码错误!'})
        except Exception, e:
            print e
            return render(request, "login.html", {'error': u'登录异常!'})
    else:
        return render(request, "login.html", {'error', u'请发送post请求'})

