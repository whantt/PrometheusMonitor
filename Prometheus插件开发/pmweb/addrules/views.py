# coding: utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from pmweb.settings import prometheusPath
from addconfig.models import Group, Host, PrometheusConfig
from addconfig.pathFunction import createHost, createGroup, updateHost, updateGroup, delHost
from models import PrometheusApplication, PrometheusRulesModel, PrometheusRules
from ruleFunction import write_file
import datetime
import random
import json
import os
import sys


redis_fixed_text = """#{'name': '{{ name }}', 'service': '{{ service }}', 'alert': '{{ alert }}', 'expr': '{{ expr }}', '_for': '{{ for }}', 'level': '{{ level }}', 'summary': '{{ summary }}', 'description': '{{ description }}'}
groups:
- name: {{ name }}
  rules:
  - alert: {{ alert }}
    expr: {{ expr }}
    for: {{ for }}
    labels:
      level: "{{ level }}"
      service: "{{ service }}"
    annotations:
      summary: "{{ summary }}"
      description: "{{ description }}"
"""


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

            rs = []
            # 获取模板信息
            pr = PrometheusRulesModel.objects.filter(rid=rmodel)
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
            hts = hosts.split(',')

            # 提交数据去重,去空
            _hosts = []
            for i in hts:
                if i not in _hosts:
                    if "" != i.strip():
                        _hosts.append(i)

            ht = Host.objects.filter(hid__in=_hosts)
            save_list = []
            for i in range(0, len(ht)):
                # FIXME 插入每个告警规则
                rname = name + ht[i].instance.replace('.', '').replace(':', '_')
                rexper = exper.replace('$instance', ht[i].instance)
                rid = 'R' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ''.join(str(random.choice(range(10))) for _ in range(10))
                prs = PrometheusRules(rid=rid, name=rname, service=service, fortime=fortime, model=model, description=description,level=level,application=application,expr=rexper,hid=ht[i].hid, status='0',modelid=modeid)
                # print ht[i].hid, ht[i].name, ht[i].instance, ht[i].groupid
                save_list.append(prs)
            PrometheusRules.objects.bulk_create(save_list)

            rs = ''
            # 数据插入成功
            for i in range(0, len(ht)):
                # FIXME 创建每台实例的告警规则文件
                rname = name + ht[i].instance.replace('.', '').replace(':', '_') + '_rule'
                rexper = exper.replace('$instance', ht[i].instance)
                alert = name + ht[i].instance.replace('.', '').replace(':', '_')
                filename = rule_path + ht[i].groupid + '/' + ht[i].name + '/' + rname + '.yml'

                rule = redis_fixed_text.replace('{{ name }}', rname)
                rule = rule.replace('{{ alert }}', alert)
                rule = rule.replace('{{ expr }}', rexper)
                rule = rule.replace('{{ for }}', fortime)
                rule = rule.replace('{{ level }}', level)
                rule = rule.replace('{{ summary }}', model)
                rule = rule.replace('{{ description }}', description)
                rule = rule.replace('{{ service }}', service)
                result = write_file(filename, rule)
                if result == 1:
                    rs += ht[i].instance + ','
            if "" == rs:
                rs = u'添加成功'
            return HttpResponse(json.dumps(rs))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'模板获取失败!'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))
