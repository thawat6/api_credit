# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class TripAuthenticationTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_trip_list(self):
        response = self.client.get(reverse('trip-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_read_trip_detail(self):
        response = self.client.get(reverse('trip-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_trip(self):
        MAP_DATA = {
            "source_location": 1,
            "name": 'Test crate trip',
            "delivery_date": '2016-12-05',
            "orders": [5],
            "carrier_classes": [1],
            "is_round_trip": 'true',
            "plan_data": "Test Data for trip",
            "plan_type": 'cost_rank'
        }
        response = self.client.post(reverse('trip-list'),
                                    MAP_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_trip(self):
        MAP_DATA = {
            "source_location": 2,
            "name": 'Test update trip',
            "delivery_date": '2017-12-05',
            "orders": [7],
            "carrier_classes": [2],
            "is_round_trip": 'false',
            "plan_data": "Test Data for trip update",
            "plan_type": 'dist_rank'
        }
        response = self.client.patch(reverse('trip-detail', args=[1]),
                                     MAP_DATA,
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_delete_trip(self):
        response = self.client.delete(reverse('trip-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TripTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_trip_list(self):
        response = self.client.get(reverse('trip-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_trip_detail(self):
        response = self.client.get(reverse('trip-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('source_location' in response.data)
        self.assertTrue('name' in response.data)
        self.assertTrue('delivery_date' in response.data)
        self.assertTrue('orders' in response.data)
        self.assertTrue('carrier_classes' in response.data)
        self.assertTrue('plan_data' in response.data)
        self.assertTrue('is_round_trip' in response.data)
        self.assertTrue('plan_type' in response.data)

    def test_can_create_trip(self):
        MAP_DATA = {
            "source_location": 1,
            "name": 'Test crate trip',
            "delivery_date": '2016-12-05',
            "orders": [5],
            "carrier_classes": [1],
            "is_round_trip": 'true',
            "plan_data": "Test Data for trip",
            "plan_type": 'cost_rank'
        }
        response = self.client.post(reverse('trip-list'),
                                    MAP_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # print('Create',dict(response.data)['count'],dict(dict(response.data)['results'][1])['name'])

    def test_can_update_trip(self):
        MAP_DATA = {
            "source_location": 2,
            "name": 'Test update trip',
            "delivery_date": '2017-12-05',
            "orders": [7],
            "carrier_classes": [2],
            "is_round_trip": 'false',
            "plan_data": "Test Data for trip update",
            "plan_type": 'dist_rank'
        }
        response = self.client.patch(reverse('trip-detail', args=[1]),
                                     MAP_DATA,
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_delete_trip(self):
        response = self.client.delete(reverse('trip-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
