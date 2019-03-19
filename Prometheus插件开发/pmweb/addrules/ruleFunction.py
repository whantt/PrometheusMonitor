# coding: utf-8

import os
import json


def write_file(filename, content):
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return 0
    except Exception, e:
        print e
        return 1

