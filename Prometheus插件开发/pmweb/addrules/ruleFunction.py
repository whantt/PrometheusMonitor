# coding: utf-8

import os
import json
from models import PrometheusApplication, PrometheusRules, PrometheusRulesModel


def write_file(filename, content):
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return 0
    except Exception, e:
        print e
        return 1

