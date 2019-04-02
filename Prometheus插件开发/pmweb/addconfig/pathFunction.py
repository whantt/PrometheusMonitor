# coding: utf-8

from models import Group, Host, PrometheusConfig
import os
import json


def createGroup(group):
    try:
        pc = PrometheusConfig.objects.filter()
        rulePath = pc[0].rule_files_path
        if not rulePath.endswith('/'):
            rulePath += '/'
            rulePath += group
        else:
            rulePath += group
        os.system("mkdir -p " + rulePath)
    except Exception, e:
        print e
        return False
    return True


def createHost(host, group):
    try:
        pc = PrometheusConfig.objects.filter()

        rulePath = pc[0].rule_files_path
        if not rulePath.endswith('/'):
            rulePath += '/'
            rulePath += group
        else:
            rulePath += group
        rulePath += '/'
        rulePath += host
        os.system("mkdir -p " + rulePath)

        filePath = pc[0].job_path
        grouppath = filePath
        if not filePath.endswith('/'):
            filePath += '/'
            filePath += group
        else:
            filePath += group
        filePath += '.yml'
        os.system("mkdir -p " + grouppath)

        # ht = Host.objects.filter(groupid=group)
        # x = []
        # for index in range(0, len(ht)):
        #     host = {}
        #     target_host = []
        #     target_host.append(ht[index].instance)
        #     host['targets'] = target_host
        #     host['labels'] = eval(ht[index].label)
        #     x.append(host)
        #
        # with open(filePath, 'w')as f:
        #     f.write(json.dumps(x, ensure_ascii=False))

    except Exception, e:
        print e
        return False
    return True


def updateGroup(name, group):
    try:
        pc = PrometheusConfig.objects.filter()
        filePath = pc[0].job_path
        if not filePath.endswith('/'):
            filePath += '/'
            newPath = filePath + name
            filePath += group
        else:
            newPath = filePath + name
            filePath += group
        filePath += '.yml'
        newPath += '.yml'
        # print "mv " + filePath + ' ' + newPath
        os.system("mv " + filePath + ' ' + newPath)

        rulePath = pc[0].rule_files_path
        if not rulePath.endswith('/'):
            rulePath += '/'
            newRule = rulePath + name
            rulePath += group
        else:
            newRule = rulePath + name
            rulePath += group
        # print "mv " + rulePath + ' ' + newRule
        os.system("mv " + rulePath + ' ' + newRule)
    except Exception, e:
        print e
        return False
    return True


def updateHost(group, host, name):
    try:
        pc = PrometheusConfig.objects.filter()

        rulePath = pc[0].rule_files_path
        if not rulePath.endswith('/'):
            rulePath += '/'
            rulePath += group
        else:
            rulePath += group
        rulePath += '/'
        newPath = rulePath + name
        rulePath += host
        os.system("mv " + rulePath + ' ' + newPath)

        filePath = pc[0].job_path
        grouppath = filePath
        if not filePath.endswith('/'):
            filePath += '/'
            filePath += group
        else:
            filePath += group
        filePath += '.yml'
        os.system("mkdir -p " + grouppath)

        ht = Host.objects.filter(groupid=group)
        x = []
        for index in range(0, len(ht)):
            host = {}
            target_host = []
            target_host.append(ht[index].instance)
            host['targets'] = target_host
            host['labels'] = eval(ht[index].label)
            x.append(host)

        with open(filePath, 'w')as f:
            f.write(json.dumps(x, ensure_ascii=False))


    except Exception, e:
        print e
        return False
    return True


# def delGroup(group):
#     try:
#         pc = PrometheusConfig.objects.filter()
#         filePath = pc[0].job_path
#         if not filePath.endswith('/'):
#             filePath += '/'
#             filePath += group
#         else:
#             filePath += group
#         os.system("mkdir -p " + filePath)
#
#         rulePath = pc[0].rule_files_path
#         if not rulePath.endswith('/'):
#             rulePath += '/'
#             rulePath += group
#         else:
#             rulePath += group
#         os.system("mkdir -p " + rulePath)
#     except Exception, e:
#         print e
#         return False
#     return True


def delHost(_file):
    os.system("rm -rf " + _file)



def delHosts(hostid):
    try:
        ht = Host.objects.filter(hid=hostid)
        host = ht[0].name
        group = ht[0].groupid

        pc = PrometheusConfig.objects.filter()

        rulePath = pc[0].rule_files_path
        if not rulePath.endswith('/'):
            rulePath += '/'
            rulePath += group
        else:
            rulePath += group
        rulePath += '/'
        rulePath += host
        os.system("rm -rf " + rulePath)

        # filePath = pc[0].job_path
        # if not filePath.endswith('/'):
        #     filePath += '/'
        #     filePath += group
        # else:
        #     filePath += group
        # os.system("mkdir -p " + filePath)

        filePath = pc[0].job_path
        grouppath = filePath
        if not filePath.endswith('/'):
            filePath += '/'
            filePath += group
        else:
            filePath += group
        filePath += '.yml'
        os.system("mkdir -p " + grouppath)

        ht = Host.objects.filter(groupid=group)
        x = []
        for index in range(0, len(ht)):
            host = {}
            target_host = []
            target_host.append(ht[index].instance)
            host['targets'] = target_host
            host['labels'] = eval(ht[index].label)
            x.append(host)

        with open(filePath, 'w')as f:
            f.write(json.dumps(x, ensure_ascii=False))

    except Exception, e:
        print e
        return False
    return True
