# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2019-03-28 06:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarmconfig', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prometheusalarm',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='\u552f\u4e00\u6807\u8bc6'),
        ),
    ]
