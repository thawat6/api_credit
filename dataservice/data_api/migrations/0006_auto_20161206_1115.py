# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 04:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_api', '0005_auto_20161206_0206'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['sequence']},
        ),
        migrations.AddField(
            model_name='orderitem',
            name='sequence',
            field=models.IntegerField(default=0),
        ),
    ]
