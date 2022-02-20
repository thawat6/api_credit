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
    tel = models.CharField(max_length=50, null=True,
                           blank=True,)

    def save(self, *args, **kwargs):
        remove_role(self.user, self.role)
        assign_role(self.user, self.role)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


STATUS_EQU_COURSE = (
    ('รอตรวจสอบ', 'รอตรวจสอบ'),
    ('ผ่าน', 'ผ่าน'),
    ('ไม่ผ่าน', 'ไม่ผ่าน'),
)


class StudentCourseStructure(models.Model):
    course_code = models.CharField(max_length=25, null=True,
                                   blank=True,)
    course_title = models.CharField(max_length=100, null=True,
                                    blank=True,)
    credit = models.IntegerField(default=0)
    description_file = models.TextField(
        null=True,
        blank=True,
    )
    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="student_course_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="student_course_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StructurePreferredCourseEnroll(models.Model):
    course_code = models.CharField(max_length=25, null=True,
                                   blank=True,)
    course_title = models.CharField(max_length=100, null=True,
                                    blank=True,)
    section = models.CharField(max_length=100, null=True,
                               blank=True,)
    lecturer = models.CharField(max_length=100, null=True,
                                blank=True,)

    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="structure_preferred_course_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="structure_preferred_course_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EquivalentCourse(models.Model):
    student_course = models.ForeignKey(StudentCourseStructure,
                                       null=True,
                                       blank=True,
                                       on_delete=models.SET_NULL)
    course_enroll = models.ForeignKey(StructurePreferredCourseEnroll,
                                      null=True,
                                      blank=True,
                                      on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=50, choices=STATUS_EQU_COURSE, default='รอตรวจสอบ')

    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="equivalent_course_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="equivalent_course_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TransferringEquivalentCourse(models.Model):
    equivalent_item = models.ManyToManyField(EquivalentCourse,
                                             blank=True,
                                             related_name="transferring_equivalent_item")
    semester = models.CharField(max_length=25, null=True,
                                blank=True,)
    academic_year = models.CharField(max_length=25, null=True,
                                     blank=True,)
    dean_faculty = models.CharField(max_length=100, null=True,
                                    blank=True,)
    name_committee1 = models.CharField(max_length=100, null=True,
                                       blank=True,)
    name_committee2 = models.CharField(max_length=100, null=True,
                                       blank=True,)
    name_committee3 = models.CharField(max_length=100, null=True,
                                       blank=True,)
    name_committee4 = models.CharField(max_length=100, null=True,
                                       blank=True,)
    is_approve_committee1 = models.BooleanField(default=False, )
    is_approve_committee2 = models.BooleanField(default=False, )
    is_approve_committee3 = models.BooleanField(default=False, )
    is_approve_committee4 = models.BooleanField(default=False, )
    advisor_name = models.CharField(max_length=100, null=True,
                                    blank=True,)
    advisor_comment = models.TextField(
        null=True,
        blank=True,
    )
    advisor_approve = models.BooleanField(default=False, )
    head_department_name = models.CharField(max_length=100, null=True,
                                            blank=True,)
    head_department_comment = models.TextField(
        null=True,
        blank=True,
    )
    head_department_approve = models.BooleanField(default=False, )
    head_educational_name = models.CharField(max_length=100, null=True,
                                             blank=True,)
    head_educational_comment = models.TextField(
        null=True,
        blank=True,
    )
    head_educational_approve = models.BooleanField(default=False, )

    created_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="transferring_equivalent_course_created_user",
                                     on_delete=models.SET_NULL)
    updated_user = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="transferring_equivalent_course_updated_user",
                                     on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
