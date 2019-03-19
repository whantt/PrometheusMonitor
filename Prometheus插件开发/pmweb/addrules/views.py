# coding: utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from pmweb.settings import prometheusPath
from addconfig.models import Group, Host, PrometheusConfig
from addconfig.pathFunction import createHost, createGroup, updateHost, updateGroup, delHost
from models import PrometheusApplication, PrometheusRulesModel, PrometheusRules
import datetime
import random
import json
import os
import sys


def createRules(request):
    return render(request, "addrules/createRules.html")


def dealRules(request):
    return render(request, "addrules/dealRules.html")


def cloneRules(request):
    return render(request, "addrules/cloneRules.html")


def addApplication(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '')
            if "" == name:
                return HttpResponse(json.dumps(u'添加失败,数据获取失败!'))

            aid = 'A' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ''.join(str(random.choice(range(10))) for _ in range(10))

            pa = PrometheusApplication(aid=aid,name=name)
            pa.save()

            return HttpResponse(json.dumps(u'添加成功!'))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'添加失败!'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))


def getApplication(request):
    if request.method == 'POST':
        try:
            pa = PrometheusApplication.objects.filter()
            rs = []
            for i in range(0, len(pa)):
                _rs = {}
                _rs['id'] = pa[i].aid
                _rs['name'] = pa[i].name
                rs.append(_rs)

            return HttpResponse(json.dumps(rs))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'添加失败!'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))


def addRules(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '')
            service = request.POST.get('service', '')
            time = request.POST.get('time', '')
            mode = request.POST.get('mode', '')
            des = request.POST.get('des', '')
            level = request.POST.get('level', '')
            application = request.POST.get('application', '')
            expr = request.POST.get('expr', '')
            print name, service, time, mode, des, level, application, expr
            rid = 'H' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ''.join(str(random.choice(range(10))) for _ in range(10))

            pr = PrometheusRulesModel(rid=rid, name=name, service=service, fortime=time, model=mode, description=des, level=level, application=application, expr=expr)
            pr.save()
            return HttpResponse(json.dumps('1'))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'添加失败!'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))


def getRulesModel(request):
    if request.method == 'POST':
        try:
            aid = request.POST.get('applicationid', '')
            pr = PrometheusRulesModel.objects.filter(application=aid)
            rs = []
            for i in range(0, len(pr)):
                _rs = {}
                _rs['id'] = pr[i].rid
                _rs['name'] = pr[i].name
                rs.append(_rs)

            return HttpResponse(json.dumps(rs))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'模板获取失败!'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))


def getAllGroups(request):
    if request.method == 'POST':
        try:
            pr = Group.objects.filter()
            rs = []
            for i in range(0, len(pr)):
                _rs = {}
                # _rs['id'] = pr[i].rid
                _rs['name'] = pr[i].name
                rs.append(_rs)

            return HttpResponse(json.dumps(rs))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'组获取失败!'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))


def getAllHosts(request):
    if request.method == 'POST':
        try:
            group = request.POST.get('group', '')
            if "" == group:
                return HttpResponse(json.dumps(u'参数错误!'))
            pr = Host.objects.filter(groupid=group)
            rs = []
            for i in range(0, len(pr)):
                _rs = {}
                _rs['id'] = pr[i].hid
                _rs['name'] = pr[i].name
                rs.append(_rs)
            print rs
            return HttpResponse(json.dumps(rs))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'主机获取失败!'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))


def addAllRules(request):
    if request.method == 'POST':
        try:
            rmodel = request.POST.get('rmodel', '')
            hosts = request.POST.get('hosts', '')
            print rmodel
            print hosts


            rs = []
            # 获取模板信息
            pr = PrometheusRulesModel.objects.filter(rid=rmodel)
            print pr
            modeid = pr[0].rid
            name = pr[0].name
            service = pr[0].service
            fortime = pr[0].fortime
            model = pr[0].model
            description = pr[0].description
            level = pr[0].level
            application = pr[0].application
            exper = pr[0].expr

            # 获取基础配置
            pc = PrometheusConfig.objects.filter()
            rule_path = pc[0].rule_files_path
            if not rule_path.endswith('/'):
                rule_path += '/'

            # 获取添加主机信息
            _hosts = hosts.split(',')
            print _hosts
            ht = Host.objects.filter(hid__in=_hosts)
            print ht
            for i in range(0, len(ht)):
                print ht[i].hid, ht[i].name, ht[i].instance, ht[i].groupid
                # FIXME 创建每台实例的告警规则文件 以及数据库batch


            # for i in range(0, len(pr)):
            #     _rs = {}
            #     _rs['id'] = pr[i].rid
            #     _rs['name'] = pr[i].name
            #     rs.append(_rs)

            return HttpResponse(json.dumps(rs))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'模板获取失败!'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))
