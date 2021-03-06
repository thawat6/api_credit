# Generated by Django 3.2.8 on 2022-02-13 06:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data_api', '0052_rename_year_level_userprofile_class_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquivalentCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('รอตรวจสอบ', 'รอตรวจสอบ'), ('ผ่าน', 'ผ่าน'), ('ไม่ผ่าน', 'ไม่ผ่าน')], default='รอตรวจสอบ', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='tel',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='TransferringEquivalentCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(blank=True, max_length=25, null=True)),
                ('academic_year', models.CharField(blank=True, max_length=25, null=True)),
                ('dean_faculty', models.CharField(blank=True, max_length=100, null=True)),
                ('name_committee1', models.CharField(blank=True, max_length=100, null=True)),
                ('name_committee2', models.CharField(blank=True, max_length=100, null=True)),
                ('name_committee3', models.CharField(blank=True, max_length=100, null=True)),
                ('name_committee4', models.CharField(blank=True, max_length=100, null=True)),
                ('is_approve_committee1', models.BooleanField(default=False)),
                ('is_approve_committee2', models.BooleanField(default=False)),
                ('is_approve_committee3', models.BooleanField(default=False)),
                ('is_approve_committee4', models.BooleanField(default=False)),
                ('advisor_name', models.CharField(blank=True, max_length=100, null=True)),
                ('advisor_comment', models.TextField(blank=True, null=True)),
                ('advisor_approve', models.BooleanField(default=False)),
                ('head_department_name', models.CharField(blank=True, max_length=100, null=True)),
                ('head_department_comment', models.TextField(blank=True, null=True)),
                ('head_department_approve', models.BooleanField(default=False)),
                ('head_educational_name', models.CharField(blank=True, max_length=100, null=True)),
                ('head_educational_comment', models.TextField(blank=True, null=True)),
                ('head_educational_approve', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transferring_equivalent_course_created_user', to=settings.AUTH_USER_MODEL)),
                ('equivalent_item', models.ManyToManyField(blank=True, related_name='transferring_equivalent_item', to='data_api.EquivalentCourse')),
                ('updated_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transferring_equivalent_course_updated_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourseStructure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(blank=True, max_length=25, null=True)),
                ('course_title', models.CharField(blank=True, max_length=100, null=True)),
                ('credit', models.IntegerField(default=0)),
                ('description_file', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_course_created_user', to=settings.AUTH_USER_MODEL)),
                ('updated_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_course_updated_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StructurePreferredCourseEnroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(blank=True, max_length=25, null=True)),
                ('course_title', models.CharField(blank=True, max_length=100, null=True)),
                ('section', models.CharField(blank=True, max_length=100, null=True)),
                ('lecturer', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='structure_preferred_course_created_user', to=settings.AUTH_USER_MODEL)),
                ('updated_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='structure_preferred_course_updated_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='equivalentcourse',
            name='course_enroll',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_api.structurepreferredcourseenroll'),
        ),
        migrations.AddField(
            model_name='equivalentcourse',
            name='created_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equivalent_course_created_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='equivalentcourse',
            name='student_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_api.studentcoursestructure'),
        ),
        migrations.AddField(
            model_name='equivalentcourse',
            name='updated_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equivalent_course_updated_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
