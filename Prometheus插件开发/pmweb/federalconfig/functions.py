# coding: utf-8
from models import PrometheusFederal
import urllib2
import json


def getFederals():
    _list = []
    try:
        pf = PrometheusFederal.objects.filter()
        for i in range(0, len(pf)):
            rs = {}
            rs['id'] = pf[i].id
            rs['name'] = pf[i].name
            rs['url'] = pf[i].url
            _list.append(rs)
    except Exception, e:
        print e
        return []
    return _list


def http_post(data, url):
    jdata = json.dumps(data, ensure_ascii=False)
    # print jdata
    req = urllib2.Request(url, jdata)       # 生成页面请求的完整数据
    response = urllib2.urlopen(req)       # 发送页面请求
    return response.read()                   # 获取服务器返回的页面信息
