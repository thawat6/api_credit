# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-12 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_api', '0014_auto_20170202_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='is_saved',
            field=models.BooleanField(default=False),
        ),
    ]
