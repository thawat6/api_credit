from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class OrderItemAuthenticationTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/order-items/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_order_item_list(self):
        response = self.client.get(reverse('order-item-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_read_order_item_detail(self):
        response = self.client.get(reverse('order-item-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('id' in response.data)
        self.assertFalse('uom' in response.data)
        self.assertFalse('quantity' in response.data)
        self.assertFalse('sequence' in response.data)
        self.assertFalse('product' in response.data)

    def test_can_delete_order_item(self):
        response = self.client.delete(reverse('order-item-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_order_item(self):
        ORDER_DATA = {"uom": 2, "quantity": 4.0, "sequence": 0, "product": 2}

        response = self.client.post(reverse('order-item-list'),
                                    ORDER_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_order_item(self):
        ORDER_DATA = {"uom": 3, "quantity": 5.0, "sequence": 0, "product": 1}
        response = self.client.put(reverse('order-item-detail', args=[1]),
                                   ORDER_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderItemTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/order-items/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_order_item_list(self):
        response = self.client.get(reverse('order-item-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_order_item_detail(self):
        response = self.client.get(reverse('order-item-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('uom' in response.data)
        self.assertTrue('quantity' in response.data)
        self.assertTrue('sequence' in response.data)
        self.assertTrue('product' in response.data)

    def test_can_delete_order_item(self):
        response = self.client.delete(reverse('order-item-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_create_order_item(self):
        ORDER_DATA = {"uom": 2, "quantity": 4.0, "sequence": 0, "product": 2}

        response = self.client.post(reverse('order-item-list'),
                                    ORDER_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_update_order_item(self):
        ORDER_DATA = {"uom": 3, "quantity": 5.0, "sequence": 0, "product": 1}
        response = self.client.put(reverse('order-item-detail', args=[1]),
                                   ORDER_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
