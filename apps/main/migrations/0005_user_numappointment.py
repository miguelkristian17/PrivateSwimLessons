# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-10-04 01:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190927_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='numAppointment',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
