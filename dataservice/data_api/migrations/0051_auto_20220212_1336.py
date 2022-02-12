# Generated by Django 3.2.8 on 2022-02-12 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_api', '0050_auto_20220212_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='faculty',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='field_of_study',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='level_of_study',
            field=models.CharField(blank=True, choices=[('ปวช', 'ระดับ ปวช.'), ('ปวส', 'ระดับ ปวส.'), ('ปตรี', 'ระดับปริญญาตรี'), ('ปโท', 'ระดับปริญญาโท'), ('ปเอก', 'ระดับปริญญาเอก')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='student_id',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='title',
            field=models.CharField(blank=True, choices=[('นาย', 'นาย'), ('นาง', 'นาง'), ('นางสาว', 'นางสาว')], max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='year_level',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
