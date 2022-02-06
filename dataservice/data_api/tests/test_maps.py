from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class mapAuthenticationTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/maps/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_map_list(self):
        response = self.client.get(reverse('map-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_read_map_detail(self):
        response = self.client.get(reverse('map-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('ways' in response.data)
        self.assertFalse('name' in response.data)

    def test_can_delete_map(self):
        response = self.client.delete(reverse('map-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_can_create_map(self):
    #     DIM_DATA = {

    #     }
    #     response = self.client.post(reverse('map-list'), DIM_DATA, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_can_update_map(self):
    #     COORD_DATA = {

    #     }
    #     response = self.client.put(reverse('map-detail', args=[1]), COORD_DATA, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class mapTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/maps/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_map_list(self):
        response = self.client.get(reverse('map-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_map_detail(self):
        response = self.client.get(reverse('map-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('ways' in response.data)
        self.assertTrue('name' in response.data)

    def test_can_delete_map(self):
        response = self.client.delete(reverse('map-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_can_create_map(self):
    #     DIM_DATA = {

    #     }
    #     response = self.client.post(reverse('map-list'), DIM_DATA, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_can_update_map(self):
    #     COORD_DATA = {

    #     }
    #     response = self.client.put(reverse('map-detail', args=[1]), COORD_DATA, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
