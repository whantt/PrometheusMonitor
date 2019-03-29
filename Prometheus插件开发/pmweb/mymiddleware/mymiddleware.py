# -*- coding:utf-8 -*-

# 标准模块
from urllib import quote

# 第三方模块
from django.http import HttpResponseRedirect
from django.shortcuts import render

import logging
# 自定义模块


class QtsAuthenticationMiddleware(object):
    def process_request(self, request):
        if request.path == '/login/' or request.path == '/load/':
            pass
        else:
            if '' != request.session.get('userName') and None is not request.session.get('userName'):
                if request.path.endswith('.html'):
                    stt = request.path.split('/')
                    return render(request, stt[-1])
                else:
                    pass
            else:
                return HttpResponseRedirect('/login/')
