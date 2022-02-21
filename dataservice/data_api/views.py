import requests
import locale
import operator
from django.http import HttpResponseNotFound
import numpy as np
import traceback
import json
from urllib.request import urlopen
import coreapi
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import routers, serializers, viewsets, generics, status, mixins
from data_api.models import UserProfile, StudentCourseStructure, StructurePreferredCourseEnroll, TransferringEquivalentCourse
from data_api.serializers import SetUserPassword, UserSerializer, UserDetailsSerializer, UpdateUserProfileSerializer, \
    StudentCourseStructureSerializer, StructurePreferredCourseEnrollSerializer, TransferringEquivalentCourseSerializer,\
    TransferringEquivalentCourseCreateSerializer


@api_view(['PATCH'])
def set_user_password(request, pk):
    if request.data['password'] != request.data['confirm_password']:
        return Response({'detail': 'Password and confirm paswword not match'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = SetUserPassword(user, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in [
                'GET',
        ]:
            return UserDetailsSerializer
        return UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UpdateUserProfileSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('role',)
    search_fields = ('full_name', 'tel'
                     )


class StudentCourseStructureViewset(viewsets.ModelViewSet):
    queryset = StudentCourseStructure.objects.all()
    serializer_class = StudentCourseStructureSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('created_user',)
    search_fields = ('course_code',
                     'course_title',
                     'course',
                     'subject', )


class StructurePreferredCourseEnrollViewset(viewsets.ModelViewSet):
    queryset = StructurePreferredCourseEnroll.objects.all()
    serializer_class = StructurePreferredCourseEnrollSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('created_user',)
    search_fields = ('course_code',
                     'course_title',
                     'course',
                     'subject', )


class TransferringEquivalentCourseViewSet(viewsets.ModelViewSet):

    queryset = TransferringEquivalentCourse.objects.all()
    serializer_class = TransferringEquivalentCourseSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('equivalent_type')
    ordering_fields = ('updated_at')
    filter_fields = ('created_user',)

    def get_serializer_class(self):
        if self.request.method in [
                'POST',
        ]:
            return TransferringEquivalentCourseCreateSerializer
        if self.request.method in [
                'PUT',
                'PATCH',
        ]:
            return TransferringEquivalentCourseCreateSerializer
        return TransferringEquivalentCourseSerializer
