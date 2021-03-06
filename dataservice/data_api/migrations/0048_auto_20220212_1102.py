# Generated by Django 3.2.8 on 2022-02-12 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_api', '0047_alter_userprofile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='file_transcrip',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('judge', 'Judge'), ('teacher', 'Teacher'), ('student', 'Student')], max_length=20),
        ),
    ]
