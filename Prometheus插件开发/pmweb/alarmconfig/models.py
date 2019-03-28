# coding: utf-8

from django.db import models


class PrometheusAlarm(models.Model):
    type = models.CharField(max_length=100, null=False, verbose_name=u'告警方式')
    url = models.CharField(max_length=1000, null=False, verbose_name=u'对接地址')
    name = models.CharField(max_length=100, null=False, verbose_name=u'告警组')
    comment = models.CharField(max_length=1000, null=False, verbose_name=u'说明')
    id = models.CharField(max_length=100, null=False, primary_key=True, verbose_name=u'唯一标识')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'alarm_url'
