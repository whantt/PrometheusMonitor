# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, make_response, Response
import sys
import json
import os
from makeFiles import makeConfig, writePrometheusConfig, writePrometheusJobFile, writePrometheusPingFile

reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)


@app.route('/', methods=['POST'])
def add():
    data = request.form
    for i in data:
        value = eval(i)
        if value['type'] == 'instance':
            _config = makeConfig(value)
            writePrometheusConfig(_config)
            writePrometheusJobFile(value)
            # print _config
        elif value['type'] == 'ip':
            writePrometheusPingFile(value['value'])
        else:
            return '1'
    return '0'


if __name__ == '__main__':
    app.run("0.0.0.0", 5001)
