from rest_framework import routers, serializers
from data_api.models import UserProfile, StudentCourseStructure, StructurePreferredCourseEnroll, EquivalentCourse, TransferringEquivalentCourse
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from drf_extra_fields.fields import Base64ImageField
import json

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('judge', 'Judge'),
    ('teacher', 'Teacher'),
    ('student', 'Student')
)


class SetUserPassword(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('password', 'confirm_password')
        write_only_fields = ('password', )
        read_only_fields = (
            'id',
            'is_staff',
            'is_superuser',
            'is_active',
            'date_joined',
        )

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES, write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    group = serializers.CharField(read_only=True)
    # profile_image = serializers.CharField(write_only=True)
    # file_transcrip = serializers.CharField(write_only=True)
    # title = serializers.CharField(write_only=True)
    # student_id = serializers.CharField(write_only=True)
    # level_of_study = serializers.CharField(write_only=True)
    # faculty = serializers.CharField(write_only=True)
    # field_of_study = serializers.CharField(write_only=True)
    # class_level = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password',
                  'confirm_password', 'email', 'role', 'group',)
        write_only_fields = ('password', )
        read_only_fields = (
            'id',
            'is_staff',
            'is_superuser',
            'is_active',
            'date_joined',
        )

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        role = validated_data.pop('role')
        # profile_image = validated_data.pop('profile_image')
        # file_transcrip = validated_data.pop('file_transcrip')
        # title = validated_data.pop('title')
        # student_id = validated_data.pop('student_id')
        # level_of_study = validated_data.pop('level_of_study')
        # faculty = validated_data.pop('faculty')
        # field_of_study = validated_data.pop('field_of_study')
        # class_level = validated_data.pop('class_level')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        user_profile = UserProfile.objects.create(
            user=user, role=role,)
        return user

    def update(self, instance, validated_data):
        user_profile = UserProfile.objects.filter(
            id=instance.id)
        # if validated_data.get('role'):
        #     role = validated_data.get('role')
        #     user_profile.update(
        #         role=role)
        # if validated_data.get('profile_image'):
        #     profile_image = validated_data.get('profile_image')
        #     user_profile.update(
        #         profile_image=profile_image)

        # if validated_data.get('title'):
        #     title = validated_data.get('title')
        #     user_profile.update(
        #         title=title)
        # if validated_data.get('student_id'):
        #     student_id = validated_data.get('student_id')
        #     user_profile.update(
        #         student_id=student_id)
        # if validated_data.get('level_of_study'):
        #     level_of_study = validated_data.get('level_of_study')
        #     user_profile.update(
        #         level_of_study=level_of_study)
        # if validated_data.get('faculty'):
        #     faculty = validated_data.get('faculty')
        #     user_profile.update(
        #         faculty=faculty)
        # if validated_data.get('field_of_study'):
        #     field_of_study = validated_data.get('field_of_study')
        #     user_profile.update(
        #         field_of_study=field_of_study)
        # if validated_data.get('class_level'):
        #     class_level = validated_data.get('class_level')
        #     user_profile.update(
        #         class_level=class_level)

        # if validated_data.get('file_transcrip'):
        #     file_transcrip = validated_data.get('file_transcrip')
        #     user_profile.update(file_transcrip=file_transcrip)
        if validated_data.get('first_name'):
            instance.first_name = validated_data.get(
                'first_name')
        if validated_data.get('last_name'):
            instance.last_name = validated_data.get(
                'last_name')
        if validated_data.get('username'):
            instance.username = validated_data.get(
                'username')
        if validated_data.get('email'):
            instance.email = validated_data.get(
                'email')

        instance.save()

        return instance

    def get_group(self, obj):
        groups = []
        for group in obj.groups.all():
            groups.append(group.name)
        return groups


class AuthGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
        )
        write_only_fields = ('password', )
        read_only_fields = (
            'id',
            'is_staff',
            'is_superuser',
            'is_active',
            'date_joined',
        )


class AuthUserSortDetailSerializer(serializers.ModelSerializer):
    groups = AuthGroupSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'groups',
        )


class UserDetailsSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    file_transcrip = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    student_id = serializers.SerializerMethodField()
    level_of_study = serializers.SerializerMethodField()
    faculty = serializers.SerializerMethodField()
    field_of_study = serializers.SerializerMethodField()
    class_level = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username',
                  'email', 'role', 'profile_image', 'file_transcrip',
                  'file_transcrip', 'title', 'student_id', 'level_of_study',
                  'faculty', 'field_of_study', 'class_level')
        write_only_fields = ('password', )
        read_only_fields = (
            'id',
            'is_staff',
            'is_superuser',
            'is_active',
            'date_joined',
        )

    def get_role(self, obj):
        role = ""
        user_profile = UserProfile.objects.filter(
            id=obj.id)

        if user_profile:
            for item_role in user_profile.values('role'):
                role = item_role
        return role

    def get_profile_image(self, obj):
        profile_image = ""
        user_profile = UserProfile.objects.filter(
            id=obj.id)

        if user_profile:
            for item_profile_image in user_profile.values('profile_image'):
                profile_image = item_profile_image
        return profile_image

    def get_file_transcrip(self, obj):
        file_transcrip = ""
        user_profile = UserProfile.objects.filter(
            id=obj.id)

        if user_profile:
            for item_file_transcrip in user_profile.values('file_transcrip'):
                file_transcrip = item_file_transcrip
        return file_transcrip

    def get_title(self, obj):
        title = ""
        user_profile = UserProfile.objects.filter(
            id=obj.id)

        if user_profile:
            for item_title in user_profile.values('title'):
                title = item_title
        return title

    def get_student_id(self, obj):
        student_id = ""
        user_profile = UserProfile.objects.filter(
            id=obj.id)

        if user_profile:
            for item_student_id in user_profile.values('student_id'):
                student_id = item_student_id
        return student_id

    def get_level_of_study(self, obj):
        level_of_study = ""
        user_profile = UserProfile.objects.filter(
            id=obj.id)

        if user_profile:
            for item_level_of_study in user_profile.values('level_of_study'):
                level_of_study = item_level_of_study
        return level_of_study

    def get_faculty(self, obj):
        faculty = ""
        user_profile = UserProfile.objects.filter(
            id=obj.id)

        if user_profile:
            for item_faculty in user_profile.values('faculty'):
                faculty = item_faculty
        return faculty

    def get_field_of_study(self, obj):
        field_of_study = ""
        user_profile = UserProfile.objects.filter(
            id=obj.id)

        if user_profile:
            for item_field_of_study in user_profile.values('field_of_study'):
                field_of_study = item_field_of_study
        return field_of_study

    def get_class_level(self, obj):
        class_level = ""
        user_profile = UserProfile.objects.filter(
            id=obj.id)

        if user_profile:
            for item_class_level in user_profile.values('class_level'):
                class_level = item_class_level
        return class_level


class VrpTokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    user = UserDetailsSerializer()

    class Meta:
        model = Token
        fields = ('key', 'user')


class ShowUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'full_name', 'role', 'title', 'student_id', 'level_of_study', 'profile_image',
                  'file_transcrip', 'faculty', 'field_of_study',
                  'class_level', 'tel')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('role', 'title', 'student_id', 'level_of_study', 'profile_image',
                  'file_transcrip', 'faculty', 'field_of_study',
                  'class_level', 'tel')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class StudentCourseStructureSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentCourseStructure
        fields = ('id', 'course_code', 'course_title', 'credit_type', 'credit', 'course',
                  'subject', 'course_year', 'grade', 'school', 'description', 'description_file', 'created_user',)
        read_only_fields = ('updated_user', 'created_at',
                            'updated_at')


class StructurePreferredCourseEnrollSerializer(serializers.ModelSerializer):

    class Meta:
        model = StructurePreferredCourseEnroll
        fields = ('id', 'course_code', 'course_title', 'credit_type', 'credit', 'course',
                  'subject', 'course_year', 'description', 'description_file', 'created_user',)
        read_only_fields = ('updated_user', 'created_at',
                            'updated_at')


class EquivalentCourseSerializer(serializers.ModelSerializer):
    student_course1 = StudentCourseStructureSerializer()
    student_course2 = StudentCourseStructureSerializer()
    student_course3 = StudentCourseStructureSerializer()
    student_course4 = StudentCourseStructureSerializer()
    student_course5 = StudentCourseStructureSerializer()
    student_course6 = StudentCourseStructureSerializer()
    course_enroll = StructurePreferredCourseEnrollSerializer()

    class Meta:
        model = EquivalentCourse
        fields = ('id', 'student_course1', 'student_course2',
                  'student_course3', 'student_course4', 'student_course5', 'student_course6',
                  'course_enroll', 'status', 'semester', )
        # exclude = ('created_user','updated_user','created_at','updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')


class EquivalentCourseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = EquivalentCourse
        exclude = ('created_user', 'updated_user', 'created_at', 'updated_at')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data['created_user'] = request.user
        orderitem = EquivalentCourse.objects.create(**validated_data)
        return orderitem


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'username', 'email',)
        write_only_fields = ('password', )
        read_only_fields = (
            'id',
            'is_staff',
            'is_superuser',
            'is_active',
            'date_joined',
        )


class TransferringEquivalentCourseSerializer(serializers.ModelSerializer):

    equivalent_item = EquivalentCourseSerializer(many=True)
    name_committee1 = UserProfileSerializer()
    name_committee2 = UserProfileSerializer()
    name_committee3 = UserProfileSerializer()
    name_committee4 = UserProfileSerializer()
    name_committee5 = UserProfileSerializer()
    name_committee6 = UserProfileSerializer()
    advisor = UserProfileSerializer()
    head_department = UserProfileSerializer()
    head_educational = UserProfileSerializer()
    deputy_dean_a_r = UserProfileSerializer()
    dean = UserProfileSerializer()
    head_academic_p_r = UserProfileSerializer()
    registrar_officer = UserProfileSerializer()
    created_user = UserProfileSerializer()
    updated_user = UserProfileSerializer()

    class Meta:
        model = TransferringEquivalentCourse
        fields = '__all__'
        # exclude = ('created_user', 'updated_user',)
        # read_only_fields = ('created_user', 'updated_user',
        #                     )


class TransferringEquivalentCourseCreateSerializer(serializers.ModelSerializer):

    equivalent_item = EquivalentCourseCreateSerializer(
        required=False, many=True)

    class Meta:
        model = TransferringEquivalentCourse
        fields = ('id', 'equivalent_type', 'equivalent_item', 'studied_from', 'number_of_equivalent',
                  'number_of_credit', 'name_committee1', 'name_committee2',
                  'name_committee3', 'name_committee4', 'name_committee5', 'name_committee6',
                  'advisor',
                  'head_department',
                  'head_educational',
                  'deputy_dean_a_r',
                  'dean',
                  'head_academic_p_r',
                  'registrar_officer',
                  'created_user',)
        read_only_fields = ('updated_user', 'created_at',
                            'updated_at')

    def create(self, validated_data):

        # user = None
        # request = self.context.get("request")

        # if request and hasattr(request, "user"):
        #     validated_data['created_user'] = request.user
        created_user = validated_data.pop('created_user')
        name_committee1 = validated_data.pop('name_committee1')
        name_committee2 = validated_data.pop('name_committee2')
        name_committee3 = validated_data.pop('name_committee3')
        name_committee4 = validated_data.pop('name_committee4')
        name_committee5 = validated_data.pop('name_committee5')
        name_committee6 = validated_data.pop('name_committee6')
        advisor = validated_data.pop('advisor')
        head_department = validated_data.pop('head_department')
        head_educational = validated_data.pop('head_educational')
        deputy_dean_a_r = validated_data.pop('deputy_dean_a_r')
        dean = validated_data.pop('dean')
        head_academic_p_r = validated_data.pop('head_academic_p_r')
        registrar_officer = validated_data.pop('registrar_officer')

        equivalent_item_data = validated_data.pop('equivalent_item')

        validated_data["created_user"] = created_user
        validated_data["name_committee1"] = name_committee1
        validated_data["name_committee2"] = name_committee2
        validated_data["name_committee3"] = name_committee3
        validated_data["name_committee4"] = name_committee4
        validated_data["name_committee5"] = name_committee5
        validated_data["name_committee6"] = name_committee6
        validated_data["advisor"] = advisor
        validated_data["head_department"] = head_department
        validated_data["head_educational"] = head_educational
        validated_data["deputy_dean_a_r"] = deputy_dean_a_r
        validated_data["dean"] = dean
        validated_data["head_academic_p_r"] = head_academic_p_r
        validated_data["registrar_officer"] = registrar_officer

        task = TransferringEquivalentCourse.objects.create(**validated_data)

        for data in equivalent_item_data:
            items = EquivalentCourse.objects.create(**data)
            task.equivalent_item.add(items)

        return task


class TransferringEquivalentCourseUpdateSerializer(serializers.ModelSerializer):
    # equivalent_item = EquivalentCourseCreateSerializer(
    #     required=False, many=True)

    class Meta:
        model = TransferringEquivalentCourse
        fields = ('id', 'equivalent_type',  'studied_from', 'number_of_equivalent',
                  'number_of_credit', 'name_committee1', 'name_committee2',
                  'name_committee3', 'name_committee4', 'name_committee5', 'name_committee6', 'is_approve_committee1',
                  'is_approve_committee2', 'is_approve_committee3', 'is_approve_committee4',
                  'is_approve_committee5', 'is_approve_committee6',
                  'advisor', 'advisor_comment', 'advisor_approve', 'advisor_date',
                  'head_department', 'head_department_comment', 'head_department_approve', 'head_department_date',
                  'head_educational',  'head_educational_comment', 'head_educational_approve', 'head_educational_date',
                  'deputy_dean_a_r', 'deputy_dean_a_r_comment', 'deputy_dean_a_r_approve', 'deputy_dean_a_r_date',
                  'dean', 'dean_comment', 'dean_approve', 'dean_date',
                  'head_academic_p_r', 'head_academic_p_r_comment', 'head_academic_p_r_date',
                  'registrar_officer', 'registrar_officer_comment', 'registrar_officer_approve', 'registrar_officer_date',
                  'is_retry', 'is_change_subject', 'is_change_school', 'is_studied')
        read_only_fields = ('created_user', 'updated_user', 'created_at',
                            'updated_at')

    def update(self, instance, validated_data):

        if validated_data.get('equivalent_type'):
            instance.equivalent_type = validated_data.get('equivalent_type')
        if validated_data.get('studied_from'):
            instance.studied_from = validated_data.get('studied_from')
        if validated_data.get('number_of_equivalent'):
            instance.number_of_equivalent = validated_data.get(
                'number_of_equivalent')
        if validated_data.get('number_of_credit'):
            instance.number_of_credit = validated_data.get('number_of_credit')

        if validated_data.get('name_committee1'):
            instance.name_committee1 = validated_data.get('name_committee1')

        if validated_data.get('name_committee2'):
            instance.name_committee2 = validated_data.get('name_committee2')

        if validated_data.get('name_committee3'):
            instance.name_committee3 = validated_data.get('name_committee3')

        if validated_data.get('name_committee4'):
            instance.name_committee4 = validated_data.get('name_committee4')

        if validated_data.get('name_committee5'):
            instance.name_committee5 = validated_data.get('name_committee5')

        if validated_data.get('name_committee6'):
            instance.name_committee6 = validated_data.get('name_committee6')

        if validated_data.get('is_approve_committee1'):
            instance.is_approve_committee1 = validated_data.get(
                'is_approve_committee1')
        if validated_data.get('is_approve_committee2'):
            instance.is_approve_committee2 = validated_data.get(
                'is_approve_committee2')
        if validated_data.get('is_approve_committee3'):
            instance.is_approve_committee3 = validated_data.get(
                'is_approve_committee3')
        if validated_data.get('is_approve_committee4'):
            instance.is_approve_committee4 = validated_data.get(
                'is_approve_committee4')
        if validated_data.get('is_approve_committee5'):
            instance.is_approve_committee5 = validated_data.get(
                'is_approve_committee5')
        if validated_data.get('is_approve_committee6'):
            instance.is_approve_committee6 = validated_data.get(
                'is_approve_committee6')

        if validated_data.get('advisor'):
            instance.advisor = validated_data.get('advisor')
        if validated_data.get('advisor_comment'):
            instance.advisor_comment = validated_data.get('advisor_comment')
        if validated_data.get('advisor_approve'):
            instance.advisor_approve = validated_data.get('advisor_approve')
        if validated_data.get('advisor_date'):
            instance.advisor_date = validated_data.get('advisor_date')

        if validated_data.get('head_department'):
            instance.head_department = validated_data.get('head_department')
        if validated_data.get('head_department_comment'):
            instance.head_department_comment = validated_data.get(
                'head_department_comment')
        if validated_data.get('head_department_approve'):
            instance.head_department_approve = validated_data.get(
                'head_department_approve')
        if validated_data.get('head_department_date'):
            instance.head_department_date = validated_data.get(
                'head_department_date')

        if validated_data.get('head_educational'):
            instance.head_educational = validated_data.get('head_educational')
        if validated_data.get('head_educational_comment'):
            instance.head_educational_comment = validated_data.get(
                'head_educational_comment')
        if validated_data.get('head_educational_approve'):
            instance.head_educational_approve = validated_data.get(
                'head_educational_approve')
        if validated_data.get('head_educational_date'):
            instance.head_educational_date = validated_data.get(
                'head_educational_date')

        if validated_data.get('deputy_dean_a_r'):
            instance.deputy_dean_a_r = validated_data.get('deputy_dean_a_r')
        if validated_data.get('deputy_dean_a_r_comment'):
            instance.deputy_dean_a_r_comment = validated_data.get(
                'deputy_dean_a_r_comment')
        if validated_data.get('deputy_dean_a_r_approve'):
            instance.deputy_dean_a_r_approve = validated_data.get(
                'deputy_dean_a_r_approve')
        if validated_data.get('deputy_dean_a_r_date'):
            instance.deputy_dean_a_r_date = validated_data.get(
                'deputy_dean_a_r_date')

        if validated_data.get('dean'):
            instance.dean = validated_data.get('dean')
        if validated_data.get('dean_comment'):
            instance.dean_comment = validated_data.get('dean_comment')
        if validated_data.get('dean_approve'):
            instance.dean_approve = validated_data.get('dean_approve')
        if validated_data.get('dean_date'):
            instance.dean_date = validated_data.get('dean_date')

        if validated_data.get('head_academic_p_r'):
            instance.head_academic_p_r = validated_data.get(
                'head_academic_p_r')
        if validated_data.get('head_academic_p_r_comment'):
            instance.head_academic_p_r_comment = validated_data.get(
                'head_academic_p_r_comment')
        if validated_data.get('head_academic_p_r_date'):
            instance.head_academic_p_r_date = validated_data.get(
                'head_academic_p_r_date')

        if validated_data.get('registrar_officer'):
            instance.registrar_officer = validated_data.get(
                'registrar_officer')
        if validated_data.get('registrar_officer_comment'):
            instance.registrar_officer_comment = validated_data.get(
                'registrar_officer_comment')
        if validated_data.get('registrar_officer_approve'):
            instance.registrar_officer_approve = validated_data.get(
                'registrar_officer_approve')
        if validated_data.get('registrar_officer_date'):
            instance.registrar_officer_date = validated_data.get(
                'registrar_officer_date')

        if validated_data.get('is_retry'):
            instance.is_retry = validated_data.get(
                'is_retry')
        if validated_data.get('is_change_subject'):
            instance.is_change_subject = validated_data.get(
                'is_change_subject')
        if validated_data.get('is_change_school'):
            instance.is_change_school = validated_data.get(
                'is_change_school')
        if validated_data.get('is_studied'):
            instance.is_studied = validated_data.get(
                'is_studied')

        # if validated_data.get('equivalent_item'):
        #     equivalent_item_data = validated_data.get('equivalent_item')

        #     for data in equivalent_item_data:
        #         items = EquivalentCourse.objects.update(**data)
        #         instance.equivalent_item.add(items)

        instance.save()
        return instance
