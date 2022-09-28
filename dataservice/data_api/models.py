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
    # ('ปโท', 'ระดับปริญญาโท'),
    # ('ปเอก', 'ระดับปริญญาเอก'),
)

TITLE_CHOICES = (
    ('นาย', 'นาย'),
    ('นาง', 'นาง'),
    ('นางสาว', 'นางสาว'),
)

SUBJECT_TASK_CHOICES = (
    ('ขอเทียบโอนรายวิชา', 'ขอเทียบโอนรายวิชา'),
    ('ขอเทียบเพื่อนเรียนแทน', 'ขอเทียบเพื่อนเรียนแทน'),
)

REGIS_OFFICER_STATE = (
    ('รอตรวจสอบ', 'รอตรวจสอบ'),
    ('ดำเนินการเรียบร้อย', 'ดำเนินการเรียบร้อย'),
    ('อื่นๆ', 'อื่นๆ'),
)

REQUIRE_CHOICES = (
    ('พ้นสถานภาพการเป็นนักศึกษาแล้วสอบกลับเข้ามาใหม่ ภายใน 6 ภาคกำรศึกษา',
     'พ้นสถานภาพการเป็นนักศึกษาแล้วสอบกลับเข้ามาใหม่ ภายใน 6 ภาคกำรศึกษา'),
    ('โอนย้ายสาขาวิชา/ย้ายเวลาเรียน', 'โอนย้ายสาขาวิชา/ย้ายเวลาเรียน'),
    ('โอนย้ายสถานศึกษา', 'โอนย้ายสถานศึกษา'),
    ('เรียนแทนรายวิชาที่เคยเรียนมาแล้ว', 'เรียนแทนรายวิชาที่เคยเรียนมาแล้ว'),
    ('อื่นๆ ', 'อื่นๆ '),

)


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='user_profile')

    full_name = models.CharField(max_length=250, null=True,
                                 blank=True,)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    title = models.CharField(max_length=25, choices=TITLE_CHOICES, null=True,
                             blank=True,)
    student_id = models.CharField(max_length=25, null=True,
                                  blank=True,)
    level_of_study = models.CharField(max_length=250, null=True,
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
        print(self.user.first_name)
        self.full_name = self.user.first_name + ' ' + self.user.last_name
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


STATUS_EQU_COURSE = (
    ('รอตรวจสอบ', 'รอตรวจสอบ'),
    ('ได้', 'ได้'),
    ('ไม่ได้', 'ไม่ได้'),
)
TYPE_CREDIT_CHOICES = (
    ('ท', 'ท'),
    ('ป', 'ป'),
    ('ร', 'ร'),
)


class StudentCourseStructure(models.Model):

    course_code = models.CharField(max_length=25, null=True,
                                   blank=True,)
    course_title = models.CharField(max_length=100, null=True,
                                    blank=True,)
    credit_type = models.CharField(
        max_length=20, choices=TYPE_CREDIT_CHOICES, default='ท')
    credit = models.IntegerField(default=0)
    course = models.CharField(max_length=250, null=True,
                              blank=True,)
    subject = models.CharField(max_length=250, null=True,
                               blank=True,)
    course_year = models.CharField(max_length=30, null=True,
                                   blank=True,)
    grade = models.CharField(max_length=30, null=True,
                             blank=True,)
    school = models.CharField(max_length=250, null=True,
                              blank=True,)
    description_file = models.TextField(
        null=True,
        blank=True,
    )
    description = models.TextField(
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
    credit_type = models.CharField(
        max_length=20, choices=TYPE_CREDIT_CHOICES, default='ท')
    credit = models.IntegerField(default=0)
    course = models.CharField(max_length=250, null=True,
                              blank=True,)
    subject = models.CharField(max_length=250, null=True,
                               blank=True,)
    course_year = models.CharField(max_length=30, null=True,
                                   blank=True,)
    description_file = models.TextField(
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    # grade = models.CharField(max_length=30, null=True,
    #                          blank=True,)
    # school = models.CharField(max_length=250, null=True,
    #                           blank=True,)
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
    credit1 = models.CharField(max_length=25, null=True,
                               blank=True,)
    credit2 = models.CharField(max_length=25, null=True,
                               blank=True,)
    credit3 = models.CharField(max_length=25, null=True,
                               blank=True,)
    credit4 = models.CharField(max_length=25, null=True,
                               blank=True,)
    credit5 = models.CharField(max_length=25, null=True,
                               blank=True,)
    credit6 = models.CharField(max_length=25, null=True,
                               blank=True,)
    remark = models.TextField(
        null=True,
        blank=True,
    )

    student_course1 = models.ForeignKey(StudentCourseStructure,
                                        related_name='student_course1',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)
    student_course2 = models.ForeignKey(StudentCourseStructure,
                                        related_name='student_course2',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)
    student_course3 = models.ForeignKey(StudentCourseStructure,
                                        related_name='student_course3',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)
    student_course4 = models.ForeignKey(StudentCourseStructure,
                                        related_name='student_course4',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)
    student_course5 = models.ForeignKey(StudentCourseStructure,
                                        related_name='student_course5',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)
    student_course6 = models.ForeignKey(StudentCourseStructure,
                                        related_name='student_course6',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)
    course_enroll = models.ForeignKey(StructurePreferredCourseEnroll,
                                      null=True,
                                      blank=True,
                                      on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=50, choices=STATUS_EQU_COURSE, default='รอตรวจสอบ')
    semester = models.CharField(max_length=30, null=True,
                                blank=True,)
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

    # ประเภท
    equivalent_type = models.CharField(
        max_length=50, choices=SUBJECT_TASK_CHOICES, default='ขอเทียบโอนรายวิชา')

    equivalent_item = models.ManyToManyField(EquivalentCourse,
                                             blank=True,
                                             related_name="transferring_equivalent_item")
    # เคยศึกษาจาก
    studied_from = models.CharField(max_length=250, null=True,
                                    blank=True,)
    # จำนวนวิชา
    number_of_equivalent = models.IntegerField(default=0, null=True)
    # จำนวนหน่วยกิจ
    number_of_credit = models.IntegerField(default=0, null=True)
    # dean_faculty = models.CharField(max_length=100, null=True,
    #                                 blank=True,)
    name_committee1 = models.ForeignKey(User,
                                        null=True,
                                        blank=True,
                                        related_name="committee1_user",
                                        on_delete=models.SET_NULL)
    name_committee2 = models.ForeignKey(User,
                                        null=True,
                                        blank=True,
                                        related_name="committee2_user",
                                        on_delete=models.SET_NULL)
    name_committee3 = models.ForeignKey(User,
                                        null=True,
                                        blank=True,
                                        related_name="committee3_user",
                                        on_delete=models.SET_NULL)
    name_committee4 = models.ForeignKey(User,
                                        null=True,
                                        blank=True,
                                        related_name="committee4_user",
                                        on_delete=models.SET_NULL)
    name_committee5 = models.ForeignKey(User,
                                        null=True,
                                        blank=True,
                                        related_name="committee5_user",
                                        on_delete=models.SET_NULL)
    name_committee6 = models.ForeignKey(User,
                                        null=True,
                                        blank=True,
                                        related_name="committee6_user",
                                        on_delete=models.SET_NULL)
    is_approve_committee1 = models.BooleanField(default=False, null=True)
    is_approve_committee2 = models.BooleanField(default=False, null=True)
    is_approve_committee3 = models.BooleanField(default=False, null=True)
    is_approve_committee4 = models.BooleanField(default=False, null=True)
    is_approve_committee5 = models.BooleanField(default=False, null=True)
    is_approve_committee6 = models.BooleanField(default=False, null=True)

    advisor = models.ForeignKey(User,
                                null=True,
                                blank=True,
                                related_name="advisor_user",
                                on_delete=models.SET_NULL)
    advisor_comment = models.TextField(
        null=True,
        blank=True,
    )
    advisor_approve = models.BooleanField(default=False, null=True)
    advisor_date = models.DateTimeField(null=True,
                                        blank=True,)

    # หัวหน้าสาขา
    head_department = models.ForeignKey(User,
                                        null=True,
                                        blank=True,
                                        related_name="head_department_user",
                                        on_delete=models.SET_NULL)
    head_department_comment = models.TextField(
        null=True,
        blank=True,
    )
    head_department_approve = models.BooleanField(default=False, null=True)
    head_department_date = models.DateTimeField(null=True,
                                                blank=True,)

    # หัวหน้างานบริการการศึกษา สำนักงานคณบดี
    head_educational = models.ForeignKey(User,
                                         null=True,
                                         blank=True,
                                         related_name="head_educational_user",
                                         on_delete=models.SET_NULL)
    head_educational_comment = models.TextField(
        null=True,
        blank=True,
    )
    head_educational_approve = models.BooleanField(default=False, null=True)
    head_educational_date = models.DateTimeField(null=True,
                                                 blank=True,)

    # รองคณบดีฝ่ายวิชาการและวิจัย
    deputy_dean_a_r = models.ForeignKey(User,
                                        null=True,
                                        blank=True,
                                        related_name="deputy_dean_a_r_user",
                                        on_delete=models.SET_NULL)
    deputy_dean_a_r_comment = models.TextField(
        null=True,
        blank=True,
    )
    deputy_dean_a_r_approve = models.BooleanField(default=False, null=True)
    deputy_dean_a_r_date = models.DateTimeField(null=True,
                                                blank=True,)

    # คณบดี
    dean = models.ForeignKey(User,
                             null=True,
                             blank=True,
                             related_name="dean_user",
                             on_delete=models.SET_NULL)
    dean_comment = models.TextField(
        null=True,
        blank=True,
    )
    dean_approve = models.BooleanField(default=False, null=True)
    dean_date = models.DateTimeField(null=True,
                                     blank=True,)

    # หัวหน้าแผนกงานส่งเสริมวิาการและงานทะเบียน
    head_academic_p_r = models.ForeignKey(User,
                                          null=True,
                                          blank=True,
                                          related_name="head_academic_p_r_user",
                                          on_delete=models.SET_NULL)
    head_academic_p_r_comment = models.TextField(
        null=True,
        blank=True,
    )
    # head_academic_p_r_approve = models.BooleanField(default=False, )
    head_academic_p_r_date = models.DateTimeField(null=True,
                                                  blank=True,)

    # เจ้าหน้าที่ทะเบียน
    registrar_officer = models.ForeignKey(User,
                                          null=True,
                                          blank=True,
                                          related_name="registrar_officer_user",
                                          on_delete=models.SET_NULL)
    registrar_officer_comment = models.TextField(
        null=True,
        blank=True,
    )
    registrar_officer_approve = models.CharField(
        max_length=50, choices=REGIS_OFFICER_STATE, default='รอตรวจสอบ', null=True)
    registrar_officer_date = models.DateTimeField(null=True,
                                                  blank=True,)
    is_retry = models.BooleanField(default=False, null=True)
    is_change_subject = models.BooleanField(default=False, null=True)
    is_change_school = models.BooleanField(default=False, null=True)
    is_studied = models.BooleanField(default=False, null=True)

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
