# coding: utf-8

from django.db import models


class PrometheusPing(models.Model):
    name = models.CharField(max_length=100, primary_key=True, null=False, unique=True, verbose_name=u'名称')
    interval = models.CharField(max_length=100, null=False, verbose_name=u'时间间隔')
    uri = models.CharField(max_length=100, null=False, verbose_name=u'uri')
    url = models.CharField(max_length=100, null=False, verbose_name=u'地址')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'ping_config'

