# coding: utf-8

from django.db import models


class PrometheusConfig(models.Model):
    name = models.CharField(max_length=100, null=False, primary_key=True, verbose_name=u'prometheus名称')
    scrape_interval = models.CharField(max_length=100, null=False, verbose_name=u'数据获取时间间隔')
    evaluation_interval = models.CharField(max_length=100, null=False, verbose_name=u'计算rule的间隔')
    scrape_timeout = models.CharField(max_length=100, null=False, verbose_name=u'超时时间')
    alertmanagers_targets = models.CharField(max_length=100, null=False, verbose_name=u'alertmanager地址')
    rule_files_path = models.CharField(max_length=100, null=False, verbose_name=u'告警规则文件路径')
    job_path = models.CharField(max_length=100, null=False, verbose_name=u'job文件路径')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'prometheus_config'


class Group(models.Model):
    # gid = models.CharField(max_length=100, unique=True, null=False, primary_key=True)
    name = models.CharField(max_length=100, null=False, unique=True)
    scrape_interval = models.CharField(max_length=100, verbose_name=u'数据获取时间间隔')
    scheme = models.CharField(max_length=100, verbose_name=u'接口方式http或https')
    insecure_skip_verify = models.CharField(max_length=100, verbose_name=u'忽略https证书验证')
    metrics_path = models.CharField(max_length=100, verbose_name=u'接口uri')
    match = models.CharField(max_length=1000, verbose_name=u'匹配')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'groupconfig'


class Host(models.Model):
    hid = models.CharField(max_length=100, unique=True, null=False, primary_key=True)
    instance = models.CharField(max_length=20, null=False, unique=True)
    name = models.CharField(max_length=100, null=False, unique=True)
    groupid = models.CharField(max_length=100, null=False)
    monitortype = models.CharField(max_length=100, null=False)
    # group = models.ManyToManyField(Group)
    label = models.CharField(max_length=1000, verbose_name=u'标签')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'hostconfig'


