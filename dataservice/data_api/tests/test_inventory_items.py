from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class InventoryItemAuthenticationTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/inventory-items/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_inventory_item_list(self):
        response = self.client.get(reverse('inventory-item-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_read_inventory_item_detail(self):
        response = self.client.get(reverse('inventory-item-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('id' in response.data)
        self.assertFalse('quantity' in response.data)
        self.assertFalse('product' in response.data)
        self.assertFalse('uom' in response.data)

    def test_can_delete_inventory_item(self):
        response = self.client.delete(
            reverse('inventory-item-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_inventory_item(self):
        INV_DATA = {"quantity": 200.0, "product": 2, "uom": 6}

        response = self.client.post(reverse('inventory-item-list'),
                                    INV_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_inventory_item(self):
        INV_DATA = {"quantity": 200.0, "product": 1, "uom": 6}
        response = self.client.put(reverse('inventory-item-detail', args=[1]),
                                   INV_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_partial_inventory_item(self):
        INV_DATA = {
            "quantity": 400.0,
        }
        response = self.client.patch(reverse('inventory-item-detail',
                                             args=[1]),
                                     INV_DATA,
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class InventoryItemTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/inventory-items/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_inventory_item_list(self):
        response = self.client.get(reverse('inventory-item-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_inventory_item_detail(self):
        response = self.client.get(reverse('inventory-item-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('quantity' in response.data)
        self.assertTrue('product' in response.data)
        self.assertTrue('uom' in response.data)

    def test_can_delete_inventory_item(self):
        response = self.client.delete(
            reverse('inventory-item-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_create_inventory_item(self):
        INV_DATA = {"quantity": 200.0, "product": 2, "uom": 6}

        response = self.client.post(reverse('inventory-item-list'),
                                    INV_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_update_inventory_item(self):
        INV_DATA = {"quantity": 200.0, "product": 1, "uom": 6}
        response = self.client.put(reverse('inventory-item-detail', args=[1]),
                                   INV_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_update_partial_inventory_item(self):
        INV_DATA = {
            "quantity": 400.0,
        }
        response = self.client.patch(reverse('inventory-item-detail',
                                             args=[1]),
                                     INV_DATA,
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
