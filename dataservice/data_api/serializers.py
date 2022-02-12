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

    def update(self, instance, validated_data):
        role = validated_data.get('role')
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
        user_profile = UserProfile.objects.filter(
            id=instance.id)

        user_profile.update(role=role)
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
        role = ""
        user_profile = UserProfile.objects.filter(
            id=obj.id)
        print(user_profile.values('role'))
        if user_profile:
            for item_role in user_profile.values('role'):
                role = item_role
        return role


class VrpTokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    user = UserDetailsSerializer()

    class Meta:
        model = Token
        fields = ('key', 'user')
