# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-15 18:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data_api', '0019_auto_20170215_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('planner', 'Planner'), ('trip_manager', 'TripManager'), ('sale_person', 'SalePerson'), ('back_office', 'BackOfficer'), ('order_manager', 'OrderManager'), ('service_admin', 'ServiceAdmin')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]