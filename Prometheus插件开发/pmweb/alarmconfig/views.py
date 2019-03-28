# coding: utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from pmweb.settings import prometheusPath
from addconfig.models import Group, Host, PrometheusConfig
from models import PrometheusAlarm
import datetime
import random
import json
import os
import sys


def toAlarm(request):
    return render(request, "alarmconfig/setAlarm.html")


def getAlarm(request):
    if request.method == 'POST':
        try:
            pageS = int(request.POST.get('page', '1'))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'查询失败'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))

    gs = PrometheusAlarm.objects.filter()
    size = len(gs)
    start = 0 + (pageS - 1)*10
    end = 10 + (pageS - 1)*10
    gs = PrometheusAlarm.objects.filter()[start:end]
    result = {}
    result['size'] = size
    if size%10 == 0:
        result['pages'] = size/10
    else:
        result['pages'] = size/10 + 1

    rs = []
    for i in range(0, len(gs)):
        _rs = {}
        _rs['id'] = gs[i].id
        _rs['name'] = gs[i].name
        _rs['type'] = gs[i].type
        _rs['url'] = gs[i].url
        _rs['des'] = gs[i].comment
        rs.append(_rs)
    result['value'] = rs
    return HttpResponse(json.dumps(result))


def submitAlarm(request):
    if request.method == 'POST':
        try:
            aid = request.POST.get('aid')
            aname = request.POST.get('aname', '')
            atype = request.POST.get('atype', '')
            aurl = request.POST.get('aurl', '')
            ades = request.POST.get('ades', '')
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'查询失败'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))

    if "" == str(aid):
        try:
            aid = 'A' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ''.join(str(random.choice(range(10))) for _ in range(10))
            pa = PrometheusAlarm(id=aid, type=atype, url=aurl, name=aname, comment=ades)
            pa.save()
            return HttpResponse(json.dumps(u'添加成功!'))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'添加失败!'))
        pass
    else:
        try:
            PrometheusAlarm.objects.filter(id=str(aid)).update(name=aname, type=atype, url=aurl, comment=ades)
            return HttpResponse(json.dumps(u'更新成功!'))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'更新失败!'))


def delAlarm(request):
    if request.method == 'POST':
        try:
            aid = request.POST.get('aid', '')
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'参数错误'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))

    if "" == aid:
        return HttpResponse(json.dumps(u'参数错误'))
    try:
        PrometheusAlarm.objects.filter(id=aid).delete()
    except Exception, e:
        print e
        return HttpResponse(json.dumps(u'删除失败!'))

    return HttpResponse(json.dumps(u'删除成功!'))