from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, Group
from rolepermissions.roles import assign_role, remove_role


ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('judge', 'Judge'),
    ('teacher', 'Teacher'),
    ('student', 'Student')
)
LEVEL_STUDY_CHOICES = (
    ('ปวช', 'ระดับ ปวช.'),
    ('ปวส', 'ระดับ ปวส.'),
    ('ปตรี', 'ระดับปริญญาตรี'),
    ('ปโท', 'ระดับปริญญาโท'),
    ('ปเอก', 'ระดับปริญญาเอก'),
)

TITLE_CHOICES = (
    ('นาย', 'นาย'),
    ('นาง', 'นาง'),
    ('นางสาว', 'นางสาว'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='user_profile')

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    title = models.CharField(max_length=25, choices=TITLE_CHOICES, null=True,
                             blank=True,)
    student_id = models.CharField(max_length=25, null=True,
                                  blank=True,)
    level_of_study = models.CharField(
        max_length=50, choices=LEVEL_STUDY_CHOICES, null=True,
        blank=True,)

    profile_image = models.TextField(
        null=True,
        blank=True,
    )

    file_transcrip = models.TextField(
        null=True,
        blank=True,
    )
    faculty = models.CharField(max_length=100, null=True,
                               blank=True,)
    field_of_study = models.CharField(max_length=100, null=True,
                                      blank=True,)
    class_level = models.CharField(max_length=20, null=True,
                                   blank=True,)

    def save(self, *args, **kwargs):
        remove_role(self.user, self.role)
        assign_role(self.user, self.role)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
