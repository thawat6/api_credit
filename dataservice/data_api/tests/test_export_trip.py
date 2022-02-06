# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class ExportTripAuthenticationTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_trip(self):
        response = self.client.get(
            reverse('exports-trip-detail', args=[1, 'csv']))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class ExportTripTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_trip(self):
        response = self.client.get(
            reverse('exports-trip-detail', args=[1, 'csv']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# class ExportPlanAuthenticationTest(APITestCase):
#
#     fixtures = ['auth.json', 'data_api.json']
#
#     def setUp(self):
#         self.client = APIClient()
#
#     def test_can_read_plan(self):
#         response = self.client.get(reverse('exports-plan-detail',args=[1,'csv']))
#         self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class ExportPlanTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_plan(self):
        response = self.client.get(
            reverse('exports-plan-detail', args=[1, 'csv']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
