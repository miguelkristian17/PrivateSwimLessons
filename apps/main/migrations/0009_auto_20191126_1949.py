# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-11-26 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20191112_0228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='timeExperience',
            field=models.TextField(blank=True, null=True),
        ),
    ]
