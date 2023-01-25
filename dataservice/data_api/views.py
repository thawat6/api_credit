import requests
import locale
import operator
import csv
import codecs
from django.http import HttpResponseNotFound
import numpy as np
import traceback
import json
from urllib.request import urlopen
import coreapi
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
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
from data_api.models import UserProfile, StudentCourseStructure, StructurePreferredCourseEnroll, CommitteeUser, TransferringEquivalentCourse
from data_api.serializers import SetUserPassword, UserSerializer, UserDetailsSerializer, UpdateUserProfileSerializer, \
    StudentCourseStructureSerializer, StructurePreferredCourseEnrollSerializer, TransferringEquivalentCourseSerializer,\
    TransferringEquivalentCourseCreateSerializer, TransferringEquivalentCourseUpdateSerializer, ShowUserProfileSerializer,\
    AllTransferringEquivalentCourseSerializer, CommitteeUserSerializer, CommitteeUserCreateSerializer
fs = FileSystemStorage(location='tmp/')


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
    serializer_class = ShowUserProfileSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('role',)
    search_fields = ('full_name', 'tel'
                     )

    def get_serializer_class(self):
        if self.request.method in [
                'POST',
        ]:
            return UpdateUserProfileSerializer
        if self.request.method in [
                'PUT',
                'PATCH',
        ]:
            return UpdateUserProfileSerializer
        return ShowUserProfileSerializer


class StudentCourseStructureViewset(viewsets.ModelViewSet):
    queryset = StudentCourseStructure.objects.all()
    serializer_class = StudentCourseStructureSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('created_user', 'status',)
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

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        """Upload data from CSV"""
        file = request.FILES["file"]

        content = file.read()  # these are bytes
        file_content = ContentFile(content)
        file_name = fs.save(
            "_tmp.csv", file_content
        )
        tmp_file = fs.path(file_name)

        csv_file = open(tmp_file, errors="ignore")
        reader = csv.reader(csv_file)
        next(reader)

        course_list = []
        for id_, row in enumerate(reader):
            (
                course_code,
                course_title,
                credit_type,
                credit,
                course,
                subject,
                course_year,
                description,

            ) = row
            course_list.append(
                StructurePreferredCourseEnroll(
                    course_code=course_code,
                    course_title=course_title,
                    credit_type=credit_type,
                    credit=credit,
                    course=course,
                    subject=subject,
                    course_year=course_year,
                    description=description,
                )
            )

        StructurePreferredCourseEnroll.objects.bulk_create(course_list)

        return Response("Successfully upload the data")

    @action(detail=False, methods=['POST'])
    def upload_data_with_validation(self, request):
        """Upload data from CSV, with validation."""
        file = request.FILES.get("file")

        reader = csv.DictReader(
            codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)

        serializer = self.serializer_class(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        course_list = []
        for row in serializer.data:
            course_list.append(
                StructurePreferredCourseEnroll(
                    course_code=row["course_code"],
                    course_title=row["course_title"],
                    credit_type=row["credit_type"],
                    credit=row["credit"],
                    course=row["course"],
                    subject=row["subject"],
                    course_year=row["course_year"],
                    description=row["description"],
                )
            )

        StructurePreferredCourseEnroll.objects.bulk_create(course_list)

        return Response("Successfully upload the data")


class TransferringEquivalentCourseViewSet(viewsets.ModelViewSet):

    queryset = TransferringEquivalentCourse.objects.all()
    serializer_class = TransferringEquivalentCourseSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ['created_user__id', 'equivalent_type', 'name_committee1__id',
                     'name_committee2__id', 'name_committee3__id', 'name_committee4__id', 'name_committee5__id',
                     'name_committee6__id']
    ordering_fields = ('updated_at')
    filter_fields = ('created_user', 'equivalent_type', 'name_committee1',
                     'name_committee2', 'name_committee3', 'name_committee4', 'name_committee5',
                     'name_committee6', 'advisor', 'head_department', 'head_educational', 'deputy_dean_a_r',
                     'dean', 'head_academic_p_r', 'registrar_officer',)

    def get_serializer_class(self):
        if self.request.method in [
                'POST',
        ]:
            return TransferringEquivalentCourseCreateSerializer
        if self.request.method in [
                'PUT',
                'PATCH',
        ]:
            return TransferringEquivalentCourseUpdateSerializer
        return TransferringEquivalentCourseSerializer


class AllTransferringEquivalentCourseViewSet(viewsets.ModelViewSet):

    queryset = TransferringEquivalentCourse.objects.all()
    serializer_class = TransferringEquivalentCourseSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ['created_user__id', 'equivalent_type', 'name_committee1__id',
                     'name_committee2__id', 'name_committee3__id', 'name_committee4__id', 'name_committee5__id',
                     'name_committee6__id']
    ordering_fields = ('updated_at')
    filter_fields = ('created_user', 'equivalent_type', 'name_committee1',
                     'name_committee2', 'name_committee3', 'name_committee4', 'name_committee5',
                     'name_committee6', 'advisor', 'head_department', 'head_educational', 'deputy_dean_a_r',
                     'dean', 'head_academic_p_r', 'registrar_officer', 'status',)

    def get_serializer_class(self):
        if self.request.method in [
                'POST',
        ]:
            return TransferringEquivalentCourseCreateSerializer
        if self.request.method in [
                'PUT',
                'PATCH',
        ]:
            return TransferringEquivalentCourseUpdateSerializer
        return AllTransferringEquivalentCourseSerializer


class CommitteeUserSerializerViewSet(viewsets.ModelViewSet):

    queryset = CommitteeUser.objects.all()
    serializer_class = CommitteeUserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CommitteeUserCreateSerializer
        return CommitteeUserSerializer
