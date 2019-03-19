# coding: utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from pmweb.settings import prometheusPath
from addconfig.models import Group, Host, PrometheusConfig
from addconfig.pathFunction import createHost, createGroup, updateHost, updateGroup, delHost
import datetime
import random
import json
import os
import sys


def showGroup(request):
    return render(request, "showconfig/showGroup.html")


def showHost(request):
    return render(request, "showconfig/showHost.html")


def showGroupInfo(request):

    if request.method == 'POST':
        try:
            pageS = int(request.POST.get('page', '1'))
        except Exception, e:
            print e
            HttpResponse(json.dumps(u'查询失败'))
    else:
        HttpResponse(json.dumps(u'请发送POST请求!'))

    gs = Group.objects.filter()
    size = len(gs)

    start = 0 + (pageS - 1)*10
    end = 10 + (pageS - 1)*10
    gs = Group.objects.filter()[start:end]
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
        _rs['scrape_interval'] = gs[i].scrape_interval
        _rs['scheme'] = gs[i].scheme
        _rs['insecure_skip_verify'] = gs[i].insecure_skip_verify
        _rs['metrics_path'] = gs[i].metrics_path
        _rs['match'] = gs[i].match
        rs.append(_rs)
    result['value'] = rs
    return HttpResponse(json.dumps(result))


def updateGroupInfo(request):
    if request.method == 'POST':
        try:
            gid = request.POST.get('gid', '1')
            gname = request.POST.get('gname', '')
            gtime = request.POST.get('gtime', '')
            gtype = request.POST.get('gtype', '')
            gcheck = request.POST.get('gcheck', '')
            guri = request.POST.get('guri', '')
            gmatch = request.POST.get('gmatch', '')
            gp = Group.objects.filter(id=int(gid))
            name = gp[0].name

            gv = Group.objects.filter(name=gname)
            if len(gv) > 0:
                return HttpResponse(json.dumps(u'主机组已存在!'))

            flag = updateGroup(gname, name)
            if flag is False:
                return HttpResponse(json.dumps(u'组文件更新失败!'))
            Group.objects.filter(id=int(gid)).update(name=gname, scrape_interval=gtime, scheme=gtype, insecure_skip_verify=gcheck, metrics_path=guri, match=gmatch)
            Host.objects.filter(groupid=name.strip()).update(groupid=gname.strip())

            # pc = PrometheusConfig.objects.filter()
            # path = pc[0].rule_files_path
            # if not path.endswith('/'):
            #     path += '/'
            # os.system('mv ' + path + name.strip() + ' ' + path + gname.strip())
            # jobfile = pc[0].job_path
            # if not jobfile.endswith('/'):
            #     jobfile += '/'
            # os.system('mv ' + jobfile + name.strip() + '.yml ' + jobfile + gname.strip() + '.yml')
            return HttpResponse(json.dumps(u'更新成功!'))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'更新失败!'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))


def delGroupInfo(request):
    if request.method == 'POST':
        try:
            gid = request.POST.get('gid', '1')

            # 获取主机组名称
            # gp = Group.objects.filter(id=int(gid))
            # name = gp[0].name
            Group.objects.filter(id=int(gid)).delete()
            return HttpResponse(json.dumps(u'删除成功!'))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'删除失败!'))

    return HttpResponse(json.dumps(u'请发送POST请求!'))


def showHostInfo(request):

    if request.method == 'POST':
        try:
            pageS = int(request.POST.get('page', '1'))
        except Exception, e:
            print e
            HttpResponse(json.dumps(u'查询失败'))
    else:
        HttpResponse(json.dumps(u'请发送POST请求!'))

    ht = Host.objects.filter()
    size = len(ht)

    start = 0 + (pageS - 1)*10
    end = 10 + (pageS - 1)*10
    # gs = Group.objects.filter()[start:end]
    ht = Host.objects.filter()[start:end]
    result = {}
    result['size'] = size
    if size%10 == 0:
        result['pages'] = size/10
    else:
        result['pages'] = size/10 + 1

    rs = []
    for i in range(0, len(ht)):
        _rs = {}
        _rs['hid'] = ht[i].hid
        _rs['instance'] = ht[i].instance
        _rs['name'] = ht[i].name
        _rs['groupid'] = ht[i].groupid
        _rs['monitortype'] = ht[i].monitortype
        _rs['label'] = ht[i].label
        rs.append(_rs)
    result['value'] = rs
    return HttpResponse(json.dumps(result))
