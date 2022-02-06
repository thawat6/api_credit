from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class orderAuthenticationTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/orders/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_order_list(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_read_order_item_list(self):
        response = self.client.get(reverse('order-list-item-list', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_read_order_location_list(self):
        response = self.client.get(
            reverse('order-list-location-list', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)


class orderTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/orders/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_order_list(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_order_detail(self):
        response = self.client.get(reverse('order-detail', args=[2]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('source_location' in response.data)
        self.assertTrue('delivery_location' in response.data)
        self.assertTrue('customer' in response.data)
        self.assertTrue('sequence' in response.data)
        self.assertTrue('status' in response.data)
        self.assertTrue('order_type' in response.data)
        self.assertTrue('delivery_date' in response.data)
        self.assertTrue('delivery_time_windows' in response.data)
        self.assertTrue('items' in response.data)

    def test_can_update_order(self):
        LOCATION_DATA = {
            "source_location": 1,
            "delivery_location": 3,
            "customer": 1,
            "sequence": 0,
            "status": "new",
            "order_type": "normal",
            "delivery_date": "2016-12-01",
            "delivery_time_windows": [2],
            "items": [1]
        }
        response = self.client.put(reverse('order-detail', args=[2]),
                                   LOCATION_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_order_item_list(self):
        response = self.client.get(reverse('order-list-item-list', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_order_location_list(self):
        response = self.client.get(
            reverse('order-list-location-list', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)
