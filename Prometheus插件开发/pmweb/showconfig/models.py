# coding: utf-8

from django.db import models


class PrometheusTriggers(models.Model):
    name = models.CharField(max_length=100, null=False, primary_key=True, verbose_name=u'触发器名称')
    expr = models.CharField(max_length=100, null=False, verbose_name=u'表达式')
    service = models.CharField(max_length=100, null=False, verbose_name=u'service分组')
    for_time = models.CharField(max_length=100, null=False, verbose_name=u'持续时间')
    level = models.CharField(max_length=100, null=False, verbose_name=u'告警级别')
    summary = models.CharField(max_length=1000, null=False, verbose_name=u'告警模板')
    description = models.CharField(max_length=1000, null=False, verbose_name=u'描述')
    hostid = models.CharField(max_length=100, null=False, verbose_name=u'所属主机')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'triggers'




