# coding: utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from pmweb.settings import prometheusPath
from addconfig.models import Group, Host, PrometheusConfig
from addconfig.pathFunction import createHost, createGroup, updateHost, updateGroup, delHost
from addrules.models import PrometheusApplication, PrometheusRules, PrometheusRulesModel
from addrules.ruleFunction import write_file
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


def showModelRule(request):
    return render(request, "showRules/showModelRule.html")


def showRule(request):
    return render(request, "showRules/showRule.html")


def getAllRules(request):
    if request.method == 'POST':
        try:
            pageS = int(request.POST.get('page', '1'))
            key_word = request.POST.get('key_word', '')
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'查询失败'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))

    type = ''
    if key_word != '':
        prm = PrometheusRulesModel.objects.filter(name=key_word)
        if len(prm) > 0:
            type = 'model'
            key_word = prm[0].rid
        else:
            type = "host"
    else:
        type = ''

    from django.db import connection, transaction
    hosts = []
    cursor = connection.cursor()
    if type == 'host':
        cursor.execute("select r.rid, r.expr, r.name, h.instance, h.name, h.groupid, r.status from rules r, hostconfig h where r.hid = h.hid and h.name like '%"+key_word+"%'")
    elif type == 'model':
        cursor.execute("select r.rid, r.expr, r.name, h.instance, h.name, h.groupid, r.status from rules r, hostconfig h where r.hid = h.hid and r.modelid= %s", [key_word])
    else:
        cursor.execute("select r.rid, r.expr, r.name, h.instance, h.name, h.groupid, r.status from rules r, hostconfig h where r.hid = h.hid ")

    row = cursor.fetchall()
    for i in row:
        info = {}
        info['rid'] = i[0]
        info['expr'] = i[1]
        info['name'] = i[2]
        info['instance'] = i[3]
        info['hostname'] = i[4]
        info['groupname'] = i[5]
        info['status'] = i[6]
        hosts.append(info)

    size = len(hosts)

    start = 0 + (pageS - 1)*10
    end = 10 + (pageS - 1)*10
    # gs = Group.objects.filter()[start:end]
    _hosts = hosts[start:end]
    result = {}
    result['size'] = size
    if size%10 == 0:
        result['pages'] = size/10
    else:
        result['pages'] = size/10 + 1

    result['value'] = _hosts

    return HttpResponse(json.dumps(result))


def getRuleInfo(request):
    rs = {'status': ''}
    if request.method == 'POST':
        try:
            rid = request.POST.get('rid', '')
        except Exception, e:
            print e
            rs['status'] = u'查询失败'
            return HttpResponse(json.dumps(rs))
    else:
        rs['status'] = u'请发送POST请求!'
        return HttpResponse(json.dumps(rs))

    if '' == rid:
        rs['status'] = u'查询失败'
        return HttpResponse(json.dumps(rs))
    try:
        prs = PrometheusRules.objects.filter(rid=rid)
        info = {}
        info['name'] = prs[0].name
        info['service'] = prs[0].service
        info['fortime'] = prs[0].fortime
        info['model'] = prs[0].model
        info['description'] = prs[0].description
        info['level'] = prs[0].level
        info['expr'] = prs[0].expr
        info['status'] = prs[0].status
        info['hid'] = prs[0].hid
        rs['status'] = 'ok'
        rs['value'] = info
        return HttpResponse(json.dumps(rs))
    except Exception, e:
        print e
        rs['status'] = u'数据加载失败!'
        return HttpResponse(json.dumps(rs))


def updateRuleInfo(request):
    if request.method == 'POST':
        try:
            rid = request.POST.get('rid', '')
            rname_old = request.POST.get('rname_old', '')
            rname = request.POST.get('rname', '')
            rservice = request.POST.get('rservice', '')
            rtime = request.POST.get('rtime', '')
            rmodel = request.POST.get('rmodel', '')
            rdes = request.POST.get('rdes', '')
            rstatus = request.POST.get('rstatus', '')
            rlevel = request.POST.get('rlevel', '')
            rexpr = request.POST.get('rexpr', '')
            rstatus_old = request.POST.get('rstatus_old', '')
            rhid = request.POST.get('rhid', '')
            # print rid,rname_old,rname,rservice,rtime,rmodel,rdes,rstatus,rlevel,rexpr,rstatus_old,rhid
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'查询失败'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))

    # 获取prometheus配置基础信息
    pc = PrometheusConfig.objects.filter()

    rule_files_path = pc[0].rule_files_path
    if not rule_files_path.endswith('/'):
        rule_files_path += '/'

    job_path = pc[0].job_path
    if not job_path.endswith('/'):
        job_path += '/'

    # 获取主机信息
    ht = Host.objects.filter(hid=rhid)
    groupname = ht[0].groupid
    hostname = ht[0].name
    instance = ht[0].instance

    fileold = rule_files_path + groupname + '/' + hostname + '/'
    # fileold += rname_old + instance.replace('.', '').replace(':', '_') + '_rule.yml'
    fileold += rname_old + '_rule.yml'

    filenew = rule_files_path + groupname + '/' + hostname + '/'
    # filenew += rname + instance.replace('.', '').replace(':', '_') + '_rule.yml'
    filenew += rname + '_rule.yml'

    alert = rname + instance.replace('.', '').replace(':', '_')

    # 修改告警规则文件内容
    rule = redis_fixed_text.replace('{{ name }}', rname)
    rule = rule.replace('{{ alert }}', alert)
    rule = rule.replace('{{ expr }}', rexpr)
    rule = rule.replace('{{ for }}', rtime)
    rule = rule.replace('{{ level }}', rlevel)
    rule = rule.replace('{{ summary }}', rmodel)
    rule = rule.replace('{{ description }}', rdes)
    rule = rule.replace('{{ service }}', rservice)
    write_file(fileold, rule)

    # 修改告警文件名
    os.system('mv ' + fileold + ' ' + filenew)

    # 修改告警状态
    if rstatus != rstatus_old and rstatus == '-1':
        filestatus = filenew + '.disable'
        os.system('mv ' + filenew + ' ' + filestatus)
    elif rstatus != rstatus_old and rstatus == '0':
        fileold = filenew + '.disable'
        os.system('mv ' + fileold + ' ' + filenew)

    # 修改数据库存储记录
    # 同时修改application,model为自定义 原applicationid,modelid的基础上加G
    PrometheusRules.objects.filter(rid=rid).update(name=rname, service=rservice, fortime=rtime, model=rmodel,
                                                   description=rdes, level=rlevel, application='G', expr=rexpr,
                                                   status=rstatus, modelid='G')

    return HttpResponse(json.dumps('修改成功'))
