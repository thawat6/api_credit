from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class productAuthenticationTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/products/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_product_list(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_read_product_detail(self):
        response = self.client.get(reverse('product-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('name' in response.data)
        self.assertFalse('uom' in response.data)
        self.assertFalse('dimension' in response.data)
        self.assertFalse('weight' in response.data)

    def test_can_delete_product(self):
        response = self.client.delete(reverse('product-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_product(self):
        DIM_DATA = {
            "name": "test1",
            "uom": 3,
            "dimension": 6,
            "weight": 1.0,
            "uom_weight": 1
        }
        response = self.client.post(reverse('product-list'),
                                    DIM_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_product(self):
        COORD_DATA = {
            "name": "test2",
            "uom": 3,
            "dimension": 6,
            "weight": 1.0,
            "uom_weight": 1
        }
        response = self.client.put(reverse('product-detail', args=[1]),
                                   COORD_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class productTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/products/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_product_list(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_product_detail(self):
        response = self.client.get(reverse('product-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('name' in response.data)
        self.assertTrue('uom' in response.data)
        self.assertTrue('dimension' in response.data)
        self.assertTrue('weight' in response.data)

    def test_can_delete_product(self):
        response = self.client.delete(reverse('product-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_create_product(self):
        DIM_DATA = {
            "name": "test1",
            "uom": 3,
            "dimension": 6,
            "weight": 1.0,
            "uom_weight": 1
        }
        response = self.client.post(reverse('product-list'),
                                    DIM_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_update_product(self):
        COORD_DATA = {
            "name": "test2",
            "uom": 3,
            "dimension": 6,
            "weight": 1.0,
            "uom_weight": 1
        }
        response = self.client.put(reverse('product-detail', args=[1]),
                                   COORD_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
