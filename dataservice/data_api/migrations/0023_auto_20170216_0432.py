# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-15 21:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('data_api', '0022_auto_20170216_0356'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Company', max_length=200)),
                ('max_carrier', models.IntegerField(default=0)),
                ('start_valid_date', models.DateField(default=datetime.datetime.now)),
                ('valid_until', models.DateField(default=datetime.datetime.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='groupsettting',
            name='group_ptr',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('trip_manager', 'TripManager'), ('sale_person', 'SalePerson'), ('back_officer', 'BackOfficer'), ('order_manager', 'OrderManager'), ('service_admin', 'ServiceAdmin')], max_length=20),
        ),
        migrations.DeleteModel(
            name='GroupSettting',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data_api.Company'),
        ),
    ]