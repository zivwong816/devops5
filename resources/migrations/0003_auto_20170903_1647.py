# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 08:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_auto_20170831_1729'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='idc',
            options={'permissions': (('view_idc', '访问 IDC 页面'),)},
        ),
    ]
