from rest_framework import routers, serializers
from data_api.models import UserProfile
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
    profile_image = serializers.CharField(write_only=True)
    file_transcrip = serializers.CharField(write_only=True)
    title = serializers.CharField(write_only=True)
    student_id = serializers.CharField(write_only=True)
    level_of_study = serializers.CharField(write_only=True)
    faculty = serializers.CharField(write_only=True)
    field_of_study = serializers.CharField(write_only=True)
    class_level = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password',
                  'confirm_password', 'email', 'role', 'group', 'profile_image',
                  'file_transcrip', 'title', 'student_id', 'level_of_study', 'faculty',
                  'field_of_study', 'class_level')
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
        profile_image = validated_data.pop('profile_image')
        file_transcrip = validated_data.pop('file_transcrip')
        title = validated_data.pop('title')
        student_id = validated_data.pop('student_id')
        level_of_study = validated_data.pop('level_of_study')
        faculty = validated_data.pop('faculty')
        field_of_study = validated_data.pop('field_of_study')
        class_level = validated_data.pop('class_level')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        user_profile = UserProfile.objects.create(
            user=user, role=role, profile_image=profile_image,
            file_transcrip=file_transcrip, title=title, student_id=student_id,
            level_of_study=level_of_study, faculty=faculty, field_of_study=field_of_study,
            class_level=class_level)
        return user

    def update(self, instance, validated_data):
        user_profile = UserProfile.objects.filter(
            id=instance.id)
        if validated_data.get('role'):
            role = validated_data.get('role')
            user_profile.update(
                role=role)
        if validated_data.get('profile_image'):
            profile_image = validated_data.get('profile_image')
            user_profile.update(
                profile_image=profile_image)

        if validated_data.get('title'):
            title = validated_data.get('title')
            user_profile.update(
                title=title)
        if validated_data.get('student_id'):
            student_id = validated_data.get('student_id')
            user_profile.update(
                student_id=student_id)
        if validated_data.get('level_of_study'):
            level_of_study = validated_data.get('level_of_study')
            user_profile.update(
                level_of_study=level_of_study)
        if validated_data.get('faculty'):
            faculty = validated_data.get('faculty')
            user_profile.update(
                faculty=faculty)
        if validated_data.get('field_of_study'):
            field_of_study = validated_data.get('field_of_study')
            user_profile.update(
                field_of_study=field_of_study)
        if validated_data.get('class_level'):
            class_level = validated_data.get('class_level')
            user_profile.update(
                class_level=class_level)

        if validated_data.get('file_transcrip'):
            file_transcrip = validated_data.get('file_transcrip')
            user_profile.update(file_transcrip=file_transcrip)
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
