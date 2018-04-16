# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('s_name', models.CharField(unique=True, max_length=30, verbose_name='\u5b66\u751f\u59d3\u540d')),
                ('s_age', models.CharField(max_length=30, verbose_name='\u5b66\u751f\u5e74\u9f84')),
                ('s_country', models.TextField(null=True, verbose_name='\u5b66\u751f\u56fd\u7c4d')),
            ],
        ),
    ]
