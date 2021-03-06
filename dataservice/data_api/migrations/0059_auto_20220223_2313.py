# Generated by Django 3.2.8 on 2022-02-23 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_api', '0058_alter_transferringequivalentcourse_registrar_officer_approve'),
    ]

    operations = [
        migrations.AddField(
            model_name='structurepreferredcourseenroll',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='structurepreferredcourseenroll',
            name='grade',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='structurepreferredcourseenroll',
            name='school',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='studentcoursestructure',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentcoursestructure',
            name='grade',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='studentcoursestructure',
            name='school',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
