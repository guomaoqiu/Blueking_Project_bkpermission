# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppPer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_code', models.CharField(unique=True, max_length=30, verbose_name='app_code')),
                ('app_name', models.CharField(max_length=30, verbose_name='app\u540d\u79f0')),
                ('app_userlist', models.TextField(null=True, verbose_name='\u7528\u6237\u5217\u8868')),
            ],
        ),
        migrations.CreateModel(
            name='PaasCon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('p_host', models.CharField(unique=True, max_length=30, verbose_name='\u4e3b\u673a')),
                ('p_pass', models.CharField(max_length=120, verbose_name='\u5bc6\u7801')),
                ('p_user', models.CharField(max_length=30, verbose_name='\u7528\u6237')),
                ('p_port', models.CharField(max_length=30, verbose_name='\u7aef\u53e3')),
            ],
        ),
    ]
