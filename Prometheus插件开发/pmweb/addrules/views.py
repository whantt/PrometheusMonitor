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
                _rs['instance'] = pr[i].instance
                rs.append(_rs)
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


def getRuleModel(request):
    if request.method == 'POST':
        try:
            rmodel = request.POST.get('rmodel', '')
            prm = PrometheusRulesModel.objects.filter(rid=rmodel)
            rs = {}
            rs['id'] = prm[0].rid
            rs['name'] = prm[0].name
            rs['service'] = prm[0].service
            rs['fortime'] = prm[0].fortime
            rs['model'] = prm[0].model
            rs['description'] = prm[0].description
            rs['level'] = prm[0].level
            rs['application'] = prm[0].application
            rs['expr'] = prm[0].expr
            return HttpResponse(json.dumps(rs))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'模板信息获取失败!'))
    return HttpResponse(json.dumps(u'请发送POST请求!'))


def updateRuleModel(request):

    if request.method == 'POST':
        try:
            rid = request.POST.get('rid', '')
            rname_old = request.POST.get('rname_old', '')
            rname = request.POST.get('rname', '')
            rservice = request.POST.get('rservice', '')
            rfortime = request.POST.get('rfortime', '')
            rmodel = request.POST.get('rmodel', '')
            rdescription = request.POST.get('rdescription', '')
            rlevel = request.POST.get('rlevel', '')
            rapplication = request.POST.get('rapplication', '')
            rexpr = request.POST.get('rexpr', '')
            # print rid, rname_old, rname, rservice, rfortime, rmodel, rdescription, rlevel, rapplication, rexpr
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'参数错误!'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))

    # 修改模板规则表
    try:
        PrometheusRulesModel.objects.filter(rid=rid).update(rid=rid, name=rname, service=rservice, fortime=rfortime,
                model=rmodel,description=rdescription,level=rlevel,
                application=rapplication,expr=rexpr)
    except Exception, e:
        print e
        return HttpResponse(json.dumps(u'模板信息数据库更新失败!'))

    # 获取所有匹配此模板的主机
    hosts = []
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute("select r.rid, r.expr, h.instance, h.name, h.groupid from rules r, hostconfig h where r.hid = h.hid and r.modelid=%s", [rid])
    row = cursor.fetchall()
    for i in row:
        info = {}
        info['rid'] = i[0]
        info['expr'] = i[1]
        info['instance'] = i[2]
        info['hostname'] = i[3]
        info['groupname'] = i[4]
        hosts.append(info)

    # 获取prometheus配置基础信息
    pc = PrometheusConfig.objects.filter()

    rule_files_path = pc[0].rule_files_path
    if not rule_files_path.endswith('/'):
        rule_files_path += '/'

    job_path = pc[0].job_path
    if not job_path.endswith('/'):
        job_path += '/'

    # 如果告警规则名称改变,那么修改告警文件名
    if rname != rname_old:
        # 修改告警规则文件名
        for _host in hosts:
            fileold = rule_files_path + _host['groupname'] + '/' + _host['hostname'] + '/'
            fileold += rname_old + _host['instance'].replace('.', '').replace(':', '_') + '_rule.yml'

            filenew = rule_files_path + _host['groupname'] + '/' + _host['hostname'] + '/'
            filenew += rname + _host['instance'].replace('.', '').replace(':', '_') + '_rule.yml'

            # 修改文件
            os.system('mv ' + fileold + ' ' + filenew)

    for _host in hosts:
        try:
            fileold = rule_files_path + _host['groupname'] + '/' + _host['hostname'] + '/'
            fileold += rname_old + _host['instance'].replace('.', '').replace(':', '_') + '_rule.yml'

            filenew = rule_files_path + _host['groupname'] + '/' + _host['hostname'] + '/'
            filenew += rname + _host['instance'].replace('.', '').replace(':', '_') + '_rule.yml'

            alert = rname + _host['instance'].replace('.', '').replace(':', '_')
            rexper = rexpr.replace('$instance', _host['instance'])

            # 修改告警规则文件内容
            rule = redis_fixed_text.replace('{{ name }}', alert)
            rule = rule.replace('{{ alert }}', alert)
            rule = rule.replace('{{ expr }}', rexper)
            rule = rule.replace('{{ for }}', rfortime)
            rule = rule.replace('{{ level }}', rlevel)
            rule = rule.replace('{{ summary }}', rmodel)
            rule = rule.replace('{{ description }}', rdescription)
            rule = rule.replace('{{ service }}', rservice)
            write_file(filenew, rule)

            # 修改数据库中存储信息
            PrometheusRules.objects.filter(rid=_host['rid']).update(name=alert, service=rservice, fortime=rfortime, model=rmodel,description=rdescription, level=rlevel,application=rapplication, expr=rexper, status='0')
        except Exception, e:
            print e
            continue
    return HttpResponse(json.dumps(u'修改完成!'))


def submitClone(request):
    if request.method == 'POST':
        try:
            targets = request.POST.get('targets', '')
            host = request.POST.get('host', '')
            print targets, host
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'参数错误!'))
    else:
        return HttpResponse(json.dumps(u'请发送POST请求!'))

    # 获取主机信息
    ht = Host.objects.filter(hid=host)
    instance = ht[0].instance
    groupname = ht[0].groupid
    hostname = ht[0].name

    print instance, groupname, hostname

    # 获取target信息
    ht = Host.objects.filter(hid=targets)
    tinstance = ht[0].instance

    print tinstance

    # 获取所有目标的监控信息
    pr = PrometheusRules.objects.filter(hid=targets)
    _list = []
    for i in range(0,len(pr)):
        rs = {}
        rs['name'] = pr[i].name
        rs['service'] = pr[i].service
        rs['fortime'] = pr[i].fortime
        rs['model'] = pr[i].model
        rs['description'] = pr[i].description
        rs['level'] = pr[i].level
        rs['application'] = pr[i].application
        rs['expr'] = pr[i].expr
        rs['modelid'] = pr[i].modelid
        _list.append(rs)

    save_list = []
    # 批量插入数据库
    for _host in _list:
        rid = 'R' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ''.join(str(random.choice(range(10))) for _ in range(10))
        tsign = tinstance.replace('.', '').replace(':', '_')
        sign = instance.replace('.', '').replace(':', '_')

        texpr = _host['expr'].replace(tinstance, instance)
        pr = PrometheusRules(rid=rid, name=_host['name'].replace(tsign, sign), service=_host['service'],
                             fortime=_host['fortime'], model=_host['model'], description=_host['description'],
                             level=_host['level'], application=_host['application'], expr=texpr, hid=host, status='0',
                             modelid=_host['modelid'])
        save_list.append(pr)
    try:
        PrometheusRules.objects.bulk_create(save_list)
    except Exception, e:
        print e
        return HttpResponse(json.dumps(u'clone信息插入失败!'))

    # 获取基础配置
    pc = PrometheusConfig.objects.filter()
    rule_path = pc[0].rule_files_path
    if not rule_path.endswith('/'):
        rule_path += '/'

    _file = rule_path + groupname + '/' + hostname + '/'
    # fileold += rname_old + _host['instance'].replace('.', '').replace(':', '_') + '_rule.yml'

    # 信息写入文件
    for _host in _list:
        tsign = tinstance.replace('.', '').replace(':', '_')
        sign = instance.replace('.', '').replace(':', '_')
        rname = _host['name'].replace(tsign, sign)
        alert = rname
        rexpr = _host['expr'].replace(tinstance, instance)

        filenew = _file + rname + '_rule.yml'

        # 修改告警规则文件内容
        rule = redis_fixed_text.replace('{{ name }}', rname)
        rule = rule.replace('{{ alert }}', alert)
        rule = rule.replace('{{ expr }}', rexpr)
        rule = rule.replace('{{ for }}', _host['fortime'])
        rule = rule.replace('{{ level }}', _host['level'])
        rule = rule.replace('{{ summary }}', _host['model'])
        rule = rule.replace('{{ description }}', _host['description'])
        rule = rule.replace('{{ service }}', _host['service'])
        write_file(filenew, rule)
    return HttpResponse(json.dumps(u'clone完成!'))