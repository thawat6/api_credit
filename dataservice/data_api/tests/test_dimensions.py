from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class DimensionAuthenticationTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/dimensions/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_dimension_list(self):
        response = self.client.get(reverse('dimension-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_read_dimension_detail(self):
        response = self.client.get(reverse('dimension-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('width' in response.data)
        self.assertFalse('height' in response.data)
        self.assertFalse('length' in response.data)

    def test_can_delete_dimension(self):
        response = self.client.delete(reverse('dimension-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_dimension(self):
        DIM_DATA = {'width': 10.0, 'height': 20.0, 'length': 30.0, 'uom': 2}
        response = self.client.post(reverse('dimension-list'),
                                    DIM_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_dimension(self):
        COORD_DATA = {
            'width': 110.0,
            'height': 210.0,
            'length': 310.0,
            'uom': 2
        }
        response = self.client.put(reverse('dimension-detail', args=[1]),
                                   COORD_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DimensionTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/dimensions/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_dimension_list(self):
        response = self.client.get(reverse('dimension-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_dimension_detail(self):
        response = self.client.get(reverse('dimension-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('width' in response.data)
        self.assertTrue('height' in response.data)
        self.assertTrue('length' in response.data)

    def test_can_delete_dimension(self):
        response = self.client.delete(reverse('dimension-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_create_dimension(self):
        DIM_DATA = {'width': 10.0, 'height': 20.0, 'length': 30.0, 'uom': 2}
        response = self.client.post(reverse('dimension-list'),
                                    DIM_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_update_dimension(self):
        COORD_DATA = {
            'width': 110.0,
            'height': 210.0,
            'length': 310.0,
            'uom': 2
        }
        response = self.client.put(reverse('dimension-detail', args=[1]),
                                   COORD_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
