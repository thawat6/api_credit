# Generated by Django 3.2.8 on 2022-02-12 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_api', '0049_auto_20220212_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='file_transcrip',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.TextField(blank=True, null=True),
        ),
    ]
