from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class MVrpapDuthenticationTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_vrp_map_list(self):
        response = self.client.get(reverse('vrp-map-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_read_vrp_map_detail(self):
        response = self.client.get(reverse('vrp-map-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_vrp_map(self):
        MAP_DATA = {"name": "Test create map", "ways": [1]}
        response = self.client.post(reverse('vrp-map-list'),
                                    MAP_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_vrp_map(self):
        MAP_DATA = {"name": "Test update map", "ways": [1]}
        response = self.client.patch(reverse('vrp-map-detail', args=[1]),
                                     MAP_DATA,
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_delete_vrp_map(self):
        response = self.client.delete(reverse('vrp-map-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class VrpMapTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_vrp_map_list(self):
        response = self.client.get(reverse('vrp-map-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_vrp_map_detail(self):
        response = self.client.get(reverse('vrp-map-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('ways' in response.data)
        self.assertTrue('name' in response.data)

    def test_can_create_vrp_map(self):
        MAP_DATA = {"name": "Test create map", "ways": [1]}
        response = self.client.post(reverse('vrp-map-list'),
                                    MAP_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # print('Create',dict(response.data)['count'],dict(dict(response.data)['results'][1])['name'])

    def test_can_update_vrp_map(self):
        MAP_DATA = {"name": "Test update map", "ways": [1]}
        response = self.client.patch(reverse('vrp-map-detail', args=[1]),
                                     MAP_DATA,
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_delete_vrp_map(self):
        response = self.client.delete(reverse('vrp-map-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)