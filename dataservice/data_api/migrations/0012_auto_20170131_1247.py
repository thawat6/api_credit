# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-31 05:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_api', '0011_customer_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrier',
            name='fixed_cost_type',
            field=models.CharField(choices=[('distance', 'Per Distance(km)'), ('trip', 'Per Trip'), ('day', 'Daily'), ('week', 'Weekly'), ('month', 'Monthly'), ('year', 'Yearly')], default='trip', max_length=10),
        ),
        migrations.AddField(
            model_name='carrier',
            name='fuel_cost_type',
            field=models.CharField(choices=[('distance', 'Per Distance(km)'), ('trip', 'Per Trip'), ('day', 'Daily'), ('week', 'Weekly'), ('month', 'Monthly'), ('year', 'Yearly')], default='distance', max_length=10),
        ),
        migrations.AddField(
            model_name='carrier',
            name='man_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='carrier',
            name='man_cost_type',
            field=models.CharField(choices=[('distance', 'Per Distance(km)'), ('trip', 'Per Trip'), ('day', 'Daily'), ('week', 'Weekly'), ('month', 'Monthly'), ('year', 'Yearly')], default='month', max_length=10),
        ),
        migrations.AddField(
            model_name='carrier',
            name='service_cost_type',
            field=models.CharField(choices=[('distance', 'Per Distance(km)'), ('trip', 'Per Trip'), ('day', 'Daily'), ('week', 'Weekly'), ('month', 'Monthly'), ('year', 'Yearly')], default='year', max_length=10),
        ),
        migrations.AddField(
            model_name='mapoutway',
            name='conversion_factor',
            field=models.FloatField(default=1.0),
        ),
    ]
