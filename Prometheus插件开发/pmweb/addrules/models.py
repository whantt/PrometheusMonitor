# coding: utf-8

from django.db import models


class PrometheusApplication(models.Model):
    aid = models.CharField(max_length=100, null=False, primary_key=True, verbose_name=u'唯一标识')
    name = models.CharField(max_length=100, null=False, unique=True, verbose_name=u'触发器名称')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'application'


class PrometheusRulesModel(models.Model):
    rid = models.CharField(max_length=100, null=False, primary_key=True, verbose_name=u'唯一标识')
    name = models.CharField(max_length=100, null=False, unique=True, verbose_name=u'触发器名称')
    service = models.CharField(max_length=100, null=False, verbose_name=u'服务')
    fortime = models.CharField(max_length=100, null=False, verbose_name=u'持续时间')
    model = models.CharField(max_length=1000, null=False, verbose_name=u'模板')
    description = models.CharField(max_length=1000, null=False, verbose_name=u'描述')
    level = models.CharField(max_length=100, null=False, verbose_name=u'告警等级')
    application = models.CharField(max_length=100, null=False, verbose_name=u'应用集')
    expr = models.CharField(max_length=1000, null=False, verbose_name=u'表达式')
    # service = models.CharField(max_length=100, null=False, verbose_name=u'服务')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'rules_model'


class PrometheusRules(models.Model):
    rid = models.CharField(max_length=100, null=False, primary_key=True, verbose_name=u'唯一标识')
    name = models.CharField(max_length=100, null=False, unique=True, verbose_name=u'触发器名称')
    service = models.CharField(max_length=100, null=False, verbose_name=u'服务')
    fortime = models.CharField(max_length=100, null=False, verbose_name=u'持续时间')
    model = models.CharField(max_length=1000, null=False, verbose_name=u'模板')
    description = models.CharField(max_length=1000, null=False, verbose_name=u'描述')
    level = models.CharField(max_length=100, null=False, verbose_name=u'告警等级')
    application = models.CharField(max_length=100, null=False, verbose_name=u'应用集')
    expr = models.CharField(max_length=1000, null=False, verbose_name=u'表达式')
    hid = models.CharField(max_length=100, null=False, verbose_name=u'主机id')
    status = models.CharField(max_length=100, null=False, verbose_name=u'状态')
    modelid = models.CharField(max_length=100, null=False, verbose_name=u'模板id')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'rules'


