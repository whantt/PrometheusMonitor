# coding: utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from models import Group, Host, PrometheusConfig
from pmweb.settings import prometheusPath
import datetime
import random
import json
import os
import sys

modelConfig="""
## {{ name }}

global:
  scrape_interval: {{ scrape_interval }} # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: {{ evaluation_interval }} # Evaluate rules every 15 seconds. The default is every 1 minute.
  scrape_timeout: {{ scrape_timeout }} # 设定抓取数据的超时时间，默认为10s

alerting:
  alertmanagers:
  - static_configs:
    - targets:
      - {{ url }}

rule_files:
  {{ rule_files }}

scrape_configs:
  {{ scrape_configs }}

"""

jobConfig = """
  - job_name: '{{ name }}'
    scrape_interval: {{ scrape_interval }}
    metrics_path: '{{ metrics_path }}'
    {{ params }}
    {{ type }}
    file_sd_configs:
    - files:
      - {{ file }}
"""

def show(request):
    print 111
    return render(request, "addconfig/setconfig.html")


def showGroup(request):
    return render(request, "addconfig/setGroup.html")


def showHost(request):
    _list = []
    gps = Group.objects.filter()
    try:
        for gp in gps:
            _list.append(gp)
    except Exception, e:
        print e
    return render(request, "addconfig/setHost.html", {"GroupList": _list})


def showK(request):
    return render(request, "addconfig/setKuernets.html")


def getPConfig(request):
    clist = {}
    try:
        pc = PrometheusConfig.objects.filter()
        if len(pc) == 0:
            clist['status'] = 0
        elif len(pc) == 1:
            clist['status'] = 1
            clist['name'] = pc[0].name
            clist['scrape_interval'] = pc[0].scrape_interval
            clist['evaluation_interval'] = pc[0].evaluation_interval
            clist['scrape_timeout'] = pc[0].scrape_timeout
            clist['alertmanagers_targets'] = pc[0].alertmanagers_targets
            clist['rule_files_path'] = pc[0].rule_files_path
            clist['job_path'] = pc[0].job_path
        else:
            clist['status'] = 2
    except Exception, e:
        print e
        clist['status'] = 3
    return HttpResponse(json.dumps(clist))


# 添加prometheus公共配置
def addPConfig(request):

    if request.method == 'POST':
        try:
            name = request.POST.get('name', '')
            interval = request.POST.get('interval', '60s')
            RInterval = request.POST.get('RInterval', '60s')
            AUrl = request.POST.get('AUrl', '')
            RPath = request.POST.get('RPath', '')
            JPath = request.POST.get('JPath', '')
            timetOut = request.POST.get('timetOut', '20s')
            pc = PrometheusConfig()
            pc.delete()
            pc = PrometheusConfig(name=name, scrape_interval=interval, evaluation_interval=RInterval, scrape_timeout=timetOut, alertmanagers_targets=AUrl, rule_files_path= RPath, job_path=JPath)
            pc.save()
            return HttpResponse(json.dumps(u'添加成功'))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'添加失败'))

    return HttpResponse(json.dumps(u'请发送POST请求'))


# 添加prometheus的组配置(job)
def addGConfig(request):

    if request.method == 'POST':
        try:
            name = request.POST.get('name', '')
            interval = request.POST.get('interval', '60s')
            type = request.POST.get('type', '60s')
            check = request.POST.get('check', '')
            match = request.POST.get('match', '')
            uri = request.POST.get('uri', '')

            if uri.strip() == '':
                uri = '/metrics'

            pc = Group.objects.filter(name=name)
            if len(pc) > 0:
                return HttpResponse(json.dumps(u'目标' + name + u'已存在'))

            pc = Group(name=name, scrape_interval=interval, scheme=type, insecure_skip_verify=check, metrics_path=uri, match=match)
            pc.save()


            return HttpResponse(json.dumps(u'添加成功'))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'添加失败'))

    return HttpResponse(json.dumps(u'请发送POST请求'))


# 添加prometheus的主机配置
def addHConfig(request):

    if request.method == 'POST':
        try:
            save_list = []
            info = request.POST.get('info', '')
            group = request.POST.get('group', '')

            value = eval(info)

            for item in value:
                target = item["targets"][0]
                try:
                    name = item['labels']['name']
                except Exception, e:
                    print e
                    name = ''

                try:
                    type = item['labels']['monitortype']
                except Exception, e:
                    print e
                    type = ''

                labels = item['labels']
                id = 'H' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ''.join(str(random.choice(range(10))) for _ in range(10))
                ht = Host(hid=id, instance=target, name=name, groupid=group, monitortype=type, label=labels )
                save_list.append(ht)
            Host.objects.bulk_create(save_list)

            pc = PrometheusConfig.objects.filter()
            path = pc[0].rule_files_path
            if not path.endswith('/'):
                path += '/'

            jobfile = pc[0].job_path
            if not jobfile.endswith('/'):
                jobfile += '/'

            os.system('mkdir -p ' + path + group + '/' + name)
            os.system('mkdir -p ' + jobfile)

            ht = Host.objects.filter(groupid=group)
            x = []
            for index in range(0, len(ht)):
                host = {}
                target_host = []
                target_host.append(ht[index].instance)
                host['targets'] = target_host
                host['labels'] = eval(ht[index].label)
                x.append(host)
                # print json.dumps(host, ensure_ascii=False)

            # print json.dumps(x, ensure_ascii=False)
            # os.system('echo "' + json.dumps(x, ensure_ascii=False) + '" > ' + path + group + '.yml')
            with open(jobfile + group + '.yml', 'w')as f:
                f.write(json.dumps(x, ensure_ascii=False))

            return HttpResponse(json.dumps(u'添加成功'))
        except Exception, e:
            print e
            return HttpResponse(json.dumps(u'添加失败'))

    return HttpResponse(json.dumps(u'请发送POST请求'))


# 预览prometheus的主机配置
def showPConfig(request):
    rs = {}
    pc = PrometheusConfig.objects.filter()
    if len(pc) != 1:
        rs['status'] = '0'
        return HttpResponse(json.dumps(rs))
    else:
        rs['status'] = '1'
    rs['config'] = makeConfig()

    return HttpResponse(json.dumps(rs))


def updatePConfig(request):
    # 获取文件内容
    try:
        filecontent = makeConfig()
        # prometheusPath
        if prometheusPath.endswith('/'):
            path = prometheusPath
        else:
            path = prometheusPath + '/'
        # os.system("echo '''" + filecontent + "''' > " + path + "prometheus.yml")
        with open(path + 'prometheus.yml', 'w')as f:
            f.write(filecontent)
        return HttpResponse(json.dumps(u'文件生成成功!'))
    except Exception, e:
        print e
        return HttpResponse(json.dumps(u'文件生成失败!'))


def makeConfig():
    try:
        # 拼接公共配置部分
        pc = PrometheusConfig.objects.filter()
        name = pc[0].name
        scrape_interval = pc[0].scrape_interval
        evaluation_interval = pc[0].evaluation_interval
        scrape_timeout = pc[0].scrape_timeout
        alertmanagers_targets = pc[0].alertmanagers_targets
        rule_files_path = pc[0].rule_files_path

        if not rule_files_path.endswith('/') :
            rule_files_path = rule_files_path + '/'

        job_path = pc[0].job_path
        if not job_path.endswith('/') :
            job_path = job_path + '/'

        _config = modelConfig
        _config = _config.replace('{{ name }}', name)
        _config = _config.replace('{{ scrape_interval }}', scrape_interval)
        _config = _config.replace('{{ evaluation_interval }}', evaluation_interval)
        _config = _config.replace('{{ scrape_timeout }}', scrape_timeout)
        _config = _config.replace('{{ url }}', alertmanagers_targets)
        #
        # print 4

        # 加载主机信息
        ht = Host.objects.filter()
        _host = {}
        for index in range(0, len(ht)):
            _h = {}
            _h['hid'] = ht[index].hid
            _h['instance'] = ht[index].instance
            _h['groupname'] = ht[index].groupid
            _h['monitortype'] = ht[index].monitortype
            _h['label'] = ht[index].label
            _host[ht[index].name] = _h

        # 加载组信息
        gp = Group.objects.filter()
        # _group = []
        rule_path = ""
        jobs = ""
        for index in range(0, len(gp)):
            # _g = {}
            # _g['groupname']  = gp[index].name
            # _g['groupinterval'] = gp[index].scrape_interval
            # _g['groupscheme'] = gp[index].scheme
            # _g['groupinsecure'] = gp[index].insecure_skip_verify
            # _g['groupmetrics'] = gp[index].metrics_path
            # _g['groupmatch'] = gp[index].match
            # _group.append(_g)

            for host in _host.keys():
                if "" == rule_path:
                    if _host[host]['groupname'] == gp[index].name:
                        rule_path = '- ' + rule_files_path + gp[index].name + '/' + host + '/*.yml'
                else:
                    if _host[host]['groupname'] == gp[index].name:
                        rule_path = rule_path + '\n  - ' + rule_files_path + gp[index].name + '/' + host + '/*.yml'

            # 修改job配置
            if "" == jobs:
                jobs = jobConfig.replace('{{ name }}', gp[index].name)
                jobs = jobs.replace('{{ scrape_interval }}', scrape_interval)

                if "" != gp[index].metrics_path:
                    jobs = jobs.replace('{{ metrics_path }}', gp[index].metrics_path)
                else:
                    jobs = jobs.replace('{{ metrics_path }}', '/metrics')

                if "" != gp[index].scheme and "https" == gp[index].scheme:
                    httpsmode = 'scheme: https'
                    httpsmode = httpsmode + '\n    tls_config:'
                    httpsmode = httpsmode + '\n      insecure_skip_verify: ' + gp[index].insecure_skip_verify
                else:
                    httpsmode = 'scheme: http'

                jobs = jobs.replace('{{ type }}', httpsmode)

                if "" != gp[index].match.strip():
                    match = 'params:'
                    match = match + '\n      match[]:'
                    for mc in gp[index].match.strip().split(','):
                        if "" != mc:
                            match = match + "\n      - '" + mc + "'"

                    jobs = jobs.replace('{{ params }}', match)
                else:
                    jobs = jobs.replace('{{ params }}', '')

                _file = job_path + gp[index].name + '.yml'
                jobs = jobs.replace('{{ file }}', _file)

            else:
                jobEx = jobConfig.replace('{{ name }}', gp[index].name)
                jobEx = jobEx.replace('{{ scrape_interval }}', scrape_interval)

                if "" != gp[index].metrics_path:
                    jobEx = jobEx.replace('{{ metrics_path }}', gp[index].metrics_path)
                else:
                    jobEx = jobEx.replace('{{ metrics_path }}', '/metrics')

                if "" != gp[index].scheme and "https" == gp[index].scheme:
                    httpsmode = 'scheme: https'
                    httpsmode = httpsmode + '\n    tls_config:'
                    httpsmode = httpsmode + '\n      insecure_skip_verify: ' + gp[index].insecure_skip_verify
                else:
                    httpsmode = 'scheme: http'

                jobEx = jobEx.replace('{{ type }}', httpsmode)

                if "" != gp[index].match.strip():
                    match = 'params:'
                    match = match + '\n      match[]:'
                    for mc in gp[index].match.strip().split(','):
                        if "" != mc:
                            match = match + "\n      - '" + mc + "'"

                    jobEx = jobEx.replace('{{ params }}', match)
                jobEx = jobEx.replace('{{ params }}', '')
                _file = job_path + gp[index].name + '.yml'
                jobEx = jobEx.replace('{{ file }}', _file)

                jobs = jobs + '\n' + jobEx

        _config = _config.replace('{{ scrape_configs }}', jobs)

        _config = _config.replace('{{ rule_files }}', rule_path)

    except Exception, e:
        print e, u'配置文件信息替换错误'
        return modelConfig
    return _config

