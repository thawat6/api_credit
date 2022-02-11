from rest_framework import routers, serializers
from data_api.models import UserProfile
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from drf_extra_fields.fields import Base64ImageField
import json

ROLE_CHOICES = (
    ('driver', 'driver'),
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

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password',
                  'confirm_password', 'email', 'role', 'group')
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
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        user_profile = UserProfile.objects.create(user=user, role=role)
        return user

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

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'role')
        write_only_fields = ('password', )
        read_only_fields = (
            'id',
            'is_staff',
            'is_superuser',
            'is_active',
            'date_joined',
        )

    def get_role(self, obj):
        groups = []
        for group in obj.groups.all():
            groups.append(group.name)
        if len(groups) > 0:
            return groups[0]


class VrpTokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    user = UserDetailsSerializer()

    class Meta:
        model = Token
        fields = ('key', 'user')
