# coding: utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from pmweb.settings import prometheusPath
from models import PrometheusFederal
from addconfig.models import Group, Host
from functions import getFederals, http_post
from forms import Forms, Dforms
import datetime
import random
import json


def tofederal(request):
    _list = getFederals()
    return render(request, "federalconfig/addfederal.html", {'result': _list, 'info': u''})


def addfederal(request):
    f = Forms(request.POST)
    if f.is_valid():
        name = f.cleaned_data['fname']
        url = f.cleaned_data['furl']
        if '' == name or '' == url:
            _list = getFederals()
            return render(request, "federalconfig/addfederal.html", {'result': _list, 'info': u'参数不能为空'})
        fid = 'F' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ''.join(str(random.choice(range(10))) for _ in range(10))
        try:
            pf = PrometheusFederal(id=fid, name=name, url=url)
            pf.save()
        except Exception, e:
            print e
            _list = getFederals()
            return render(request, "federalconfig/addfederal.html", {'result': _list, 'info': u'数据插入异常'})
    else:
        _list = getFederals()
        return render(request, "federalconfig/addfederal.html", {'result': _list, 'info': u'参数异常'})
    _list = getFederals()
    return render(request, "federalconfig/addfederal.html", {'result': _list, 'info': u'添加成功'})


def delFederal(request):
    f = Dforms(request.POST)
    if f.is_valid():
        fid = f.cleaned_data['fid']
        try:
            PrometheusFederal.objects.filter(id=fid).delete()
        except Exception, e:
            print e
            _list = getFederals()
            return render(request, "federalconfig/addfederal.html", {'result': _list, 'info': u'删除失败'})
    else:
        _list = getFederals()
        return render(request, "federalconfig/addfederal.html", {'result': _list, 'info': u'删除失败'})
    _list = getFederals()
    return render(request, "federalconfig/addfederal.html", {'result': _list, 'info': u'删除成功'})


def updateFederal(request):
    try:
        _rs = {'type': 'instance'}
        _ping = {'type': 'ip'}
        f = Dforms(request.POST)
        if f.is_valid():
            fid = f.cleaned_data['fid']
        else:
            return HttpResponse(json.dumps(u'参数错误!'))
        g = Group.objects.filter(federalid=fid)
        _prs = []
        for j in range(0, len(g)):
            # rs[g[i].name] = []
            ht = Host.objects.filter(groupid=g[j].name)
            _hrs = []
            # _prs = []
            scrape_interval = g[j].scrape_interval
            scheme = g[j].scheme
            insecure_skip_verify = g[j].insecure_skip_verify
            metrics_path = g[j].metrics_path
            match = g[j].match

            for i in range(0, len(ht)):
                hrs = {}
                prs = {}
                hrs['targets'] = [ht[i].instance]
                hrs['labels'] = eval(ht[i].label)
                _hrs.append(hrs)
                _ip = ht[i].instance.split(':')[0]
                label = eval(ht[i].label)
                hostname = label['name']
                if prs.has_key(_ip) and prs[_ip] == hostname:
                    continue
                prs['targets'] = [_ip]
                prs['labels'] = eval(ht[i].label)
                prs['labels']['platform'] = g[j].name
                prs['labels']['monitortype'] = 'ping'
                _prs.append(prs)
            _rs[g[j].name] = {}
            _rs[g[j].name]['value'] = _hrs
            _rs[g[j].name]['scrape_interval'] = scrape_interval
            _rs[g[j].name]['scheme'] = scheme
            _rs[g[j].name]['insecure_skip_verify'] = insecure_skip_verify
            _rs[g[j].name]['metrics_path'] = metrics_path
            _rs[g[j].name]['match'] = match
            # _ping[g[j].name] = _prs
        _ping['value'] = _prs
    except Exception, e:
        print e
        return HttpResponse(json.dumps(u'数据错误!'))

    pf = PrometheusFederal.objects.filter(id=fid)
    _url = pf[0].url

    try:
        status = http_post(_rs, _url)
        if status == '1':
            return HttpResponse(json.dumps(u'instance数据刷新失败!'))
    except Exception, e:
        print e
        return HttpResponse(json.dumps(u'instance数据刷新失败!'))

    try:
        status = http_post(_ping, _url)
        if status == '1':
            return HttpResponse(json.dumps(u'ping数据刷新失败!'))
    except Exception, e:
        print e
        return HttpResponse(json.dumps(u'ping数据刷新失败!'))

    return HttpResponse(json.dumps(u'刷新成功!'))

