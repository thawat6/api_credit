# Generated by Django 3.2.8 on 2022-02-21 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_api', '0054_auto_20220221_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='full_name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]