from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class tripAuthenticationTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/trips/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_trip_list(self):
        response = self.client.get(reverse('trip-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_read_trip_detail(self):
        response = self.client.get(reverse('trip-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('orders' in response.data)
        self.assertFalse('name' in response.data)
        self.assertFalse('delivery_date' in response.data)
        self.assertFalse('source_location' in response.data)

    def test_can_read_trip_list(self):
        response = self.client.get(reverse('location-list-item-list',
                                           args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_delete_trip(self):
        response = self.client.delete(reverse('trip-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class tripTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/trips/
    '''
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
        self.assertTrue('orders' in response.data)
        self.assertTrue('name' in response.data)
        self.assertTrue('delivery_date' in response.data)
        self.assertTrue('source_location' in response.data)

    def test_can_read_trip_list(self):
        response = self.client.get(reverse('location-list-item-list',
                                           args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_delete_trip(self):
        response = self.client.delete(reverse('trip-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
