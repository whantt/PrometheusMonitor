# coding: utf-8

from django.db import models


class PrometheusFederal(models.Model):
    id = models.CharField(max_length=100, null=False, primary_key=True, verbose_name=u'唯一标识')
    name = models.CharField(max_length=100, null=False, verbose_name=u'名称')
    url = models.CharField(max_length=100, null=False, verbose_name=u'地址')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'federal'
