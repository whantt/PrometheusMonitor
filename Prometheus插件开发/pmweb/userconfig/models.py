# coding: utf-8

from django.db import models


class PrometheusUser(models.Model):
    uid = models.CharField(max_length=100, primary_key=True, null=False, unique=True, verbose_name=u'唯一标识')
    name = models.CharField(max_length=100, null=False, unique=True, verbose_name=u'名称')
    passwd = models.CharField(max_length=100, null=False, verbose_name=u'密码')
    # groupid = models.CharField(max_length=100, null=False, verbose_name=u'属组')
    status = models.CharField(max_length=100, null=False, verbose_name=u'状态')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'userconfig'

