from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class CarrierClassAuthenticationTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/carrier-classes/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_carrier_class_list(self):
        response = self.client.get(reverse('carrier-class-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_read_carrier_class_detail(self):
        response = self.client.get(reverse('carrier-class-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_delete_carrier_class(self):
        response = self.client.delete(reverse('carrier-class-detail',
                                              args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_carrier_class(self):
        CR_DATA = {
            "carrier_type": 1,
            "dimension": 1,
            "weight_cap": 7.0,
            "uom": 1,
        }
        response = self.client.post(reverse('carrier-class-list'),
                                    CR_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_carrier_class(self):
        CR_DATA = {
            "carrier_type": 1,
            "dimension": 2,
            "weight_cap": 5.0,
            "uom": 1,
        }
        response = self.client.put(reverse('carrier-class-detail', args=[1]),
                                   CR_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CarrierClassTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/carrier-classes/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_carrier_class_list(self):
        response = self.client.get(reverse('carrier-class-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_carrier_class_detail(self):
        response = self.client.get(reverse('carrier-class-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_delete_carrier_class(self):
        response = self.client.delete(reverse('carrier-class-detail',
                                              args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_create_carrier_class(self):
        CR_DATA = {
            "carrier_type": 1,
            "dimension": 1,
            "weight_cap": 7.0,
            "uom": 1,
        }
        response = self.client.post(reverse('carrier-class-list'),
                                    CR_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_update_carrier_class(self):
        CR_DATA = {
            "carrier_type": 1,
            "dimension": 2,
            "weight_cap": 5.0,
            "uom": 1,
        }
        response = self.client.put(reverse('carrier-class-detail', args=[1]),
                                   CR_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
