# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class CarrierAuthenticationTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/carriers/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_carrier_list(self):
        response = self.client.get(reverse('carrier-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_read_carrier_detail(self):
        response = self.client.get(reverse('carrier-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('name' in response.data)
        self.assertFalse('carrier_class' in response.data)
        self.assertFalse('fuel_cost' in response.data)
        self.assertFalse('service_cost' in response.data)
        self.assertFalse('fixed_cost' in response.data)
        self.assertFalse('location' in response.data)
        self.assertFalse('is_occupied' in response.data)

    def test_can_delete_carrier(self):
        response = self.client.delete(reverse('carrier-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_carrier(self):
        CR_DATA = {
            "name": "ปอ 9876 ขอนแก่น",
            "carrier_class": 2,
            "fuel_cost": "0.50",
            "service_cost": "0.15",
            "fixed_cost": "10000.00",
            "location": 1,
            "is_occupied": False
        }
        response = self.client.post(reverse('carrier-list'),
                                    CR_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_carrier(self):
        CR_DATA = {
            "name": "ปอ 9876 ขอนแก่น",
            "carrier_class": 1,
            "fuel_cost": "0.10",
            "service_cost": "1.15",
            "fixed_cost": "12000.00",
            "location": 2,
            "is_occupied": False
        }
        response = self.client.put(reverse('carrier-detail', args=[1]),
                                   CR_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CarrierTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/carriers/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_create_carrier(self):
        CR_DATA = {
            "name": "ปอ 9876 ขอนแก่น",
            "carrier_class": 2,
            "fuel_cost": "0.50",
            "service_cost": "0.15",
            "fixed_cost": "10000.00",
            "location": 1,
            "is_occupied": False
        }
        response = self.client.post(reverse('carrier-list'),
                                    CR_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_read_carrier_list(self):
        response = self.client.get(reverse('carrier-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_carrier_detail(self):
        response = self.client.get(reverse('carrier-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('name' in response.data)
        self.assertTrue('carrier_class' in response.data)
        self.assertTrue('fuel_cost' in response.data)
        self.assertTrue('service_cost' in response.data)
        self.assertTrue('fixed_cost' in response.data)
        self.assertTrue('location' in response.data)
        self.assertTrue('is_occupied' in response.data)

    def test_can_update_carrier(self):
        CR_DATA = {
            "name": "ปอ 9876 ขอนแก่น",
            "carrier_class": 1,
            "fuel_cost": "0.10",
            "service_cost": "1.15",
            "fixed_cost": "12000.00",
            "location": 2,
            "is_occupied": False
        }
        response = self.client.put(reverse('carrier-detail', args=[1]),
                                   CR_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_delete_carrier(self):
        response = self.client.delete(reverse('carrier-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
