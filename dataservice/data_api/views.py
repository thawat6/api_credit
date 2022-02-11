from rest_framework import routers, serializers, viewsets, generics, status, mixins
from data_api.models import UserProfile
from data_api.serializers import SetUserPassword, UserSerializer, UserDetailsSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
import coreapi
from urllib.request import urlopen
import json
import traceback
import numpy as np
from django.http import HttpResponseNotFound
import operator
import locale

import requests


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
