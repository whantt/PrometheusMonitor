# coding: utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from pmweb.settings import prometheusPath
from addconfig.models import Group, Host, PrometheusConfig
from addconfig.pathFunction import createHost, createGroup, updateHost, updateGroup, delHost
from addrules.ruleFunction import write_file
from models import PrometheusPing
import datetime
import random
import json
import os
import sys


def addconfig(request):
    return render(request, "netconfig/addPing.html")


def addconfigs(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '')
            interval = request.POST.get('interval', '')
            uri = request.POST.get('uri', '')
            url = request.POST.get('url', '')
            # print name, interval, uri, url
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'参数错误!'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))

    if "" == name or "" == url or "" == interval:
        return HttpResponse(json.dumps(u'参数错误!'))

    if "" == uri.strip():
        uri = '/probe'

    # 加载基础配置信息
    # pc = PrometheusConfig.objects.filter()
    # rulepath = pc[0].rule_files_path
    # if not rulepath.endswith('/'):
    #     rulepath += '/'

    try:
        pp = PrometheusPing()
        pp.delete()
        pp = PrometheusPing(name=name, interval=interval, uri=uri, url=url)
        pp.save()
        # os.system('mkdir -p ' + rulepath + name)
    except Exception, e:
        print e
        return HttpResponse(json.dumps(u'数据存储错误!'))

    return HttpResponse(json.dumps(u'设置成功!'))


def getconfigs(request):
    rs = {}
    rs['status'] = 1
    if request.method == 'POST':
        try:
            pp = PrometheusPing.objects.filter()
            if len(pp) > 0:
                rs['status'] = 1
                rs['name'] = pp[0].name
                rs['interval'] = pp[0].interval
                rs['uri'] = pp[0].uri
                rs['url'] = pp[0].url
            else:
                rs['status'] = 0
        except Exception, e:
            print e
            rs['status'] = 2
            return HttpResponse(json.dumps(rs))
    else:
        rs['status'] = 3
        return HttpResponse(json.dumps(rs))
    return HttpResponse(json.dumps(rs))
