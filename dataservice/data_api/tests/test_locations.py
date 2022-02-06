# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class LocationAuthenticationTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/locations/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_location_list(self):
        response = self.client.get(reverse('location-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_read_location_detail(self):
        response = self.client.get(reverse('location-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('id' in response.data)
        self.assertFalse('coord' in response.data)
        self.assertFalse('time_windows' in response.data)
        self.assertFalse('items' in response.data)

    def test_can_read_location_item_list(self):
        response = self.client.get(reverse('location-list-item-list',
                                           args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_delete_location(self):
        response = self.client.delete(reverse('location-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_location(self):
        LOCATION_DATA = {
            "coord": 1,
            "time_windows": [1, 2],
            "items": [1, 2],
            "name": "คลังสินค้า Jump",
            "location_type": "warehouse"
        }

        response = self.client.post(reverse('location-list'),
                                    LOCATION_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_location(self):
        LOCATION_DATA = {
            "coord": 2,
            "time_windows": [2],
            "items": [2],
            "name": "คลังสินค้า Jump2",
            "location_type": "warehouse"
        }
        response = self.client.put(reverse('location-detail', args=[1]),
                                   LOCATION_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_partial_update_location(self):
        LOCATION_DATA = {"time_windows": [1, 2], "items": [1]}
        response = self.client.patch(reverse('location-detail', args=[1]),
                                     LOCATION_DATA,
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LocationTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/locations/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_location_list(self):
        response = self.client.get(reverse('location-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_location_detail(self):
        response = self.client.get(reverse('location-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('coord' in response.data)
        self.assertTrue('time_windows' in response.data)
        self.assertTrue('items' in response.data)

    def test_can_read_location_item_list(self):
        response = self.client.get(reverse('location-list-item-list',
                                           args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_delete_location(self):
        response = self.client.delete(reverse('location-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_create_location(self):
        LOCATION_DATA = {
            "coord": 1,
            "time_windows": [1, 2],
            "items": [1, 2],
            "name": "คลังสินค้า Jump",
            "location_type": "warehouse"
        }

        response = self.client.post(reverse('location-list'),
                                    LOCATION_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_update_location(self):
        LOCATION_DATA = {
            "coord": 2,
            "time_windows": [2],
            "items": [2],
            "name": "คลังสินค้า Jump2",
            "location_type": "warehouse"
        }
        response = self.client.put(reverse('location-detail', args=[1]),
                                   LOCATION_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_partial_update_location(self):
        LOCATION_DATA = {"time_windows": [1, 2], "items": [1]}
        response = self.client.patch(reverse('location-detail', args=[1]),
                                     LOCATION_DATA,
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
