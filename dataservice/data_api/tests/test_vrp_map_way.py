from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class VrpMapWayDAuthenticationTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_vrp_map_way_list(self):
        response = self.client.get(reverse('vrp-map-way-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_read_vrp_map_way_detail(self):
        response = self.client.get(reverse('vrp-map-way-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_vrp_map_way(self):
        MAP_DATA = {"source_location": 1}
        response = self.client.post(reverse('vrp-map-way-list'),
                                    MAP_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_vrp_map_way(self):
        MAP_DATA = {"output_ways": [1]}
        response = self.client.patch(reverse('vrp-map-way-detail', args=[1]),
                                     MAP_DATA,
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_delete_vrp_map_way(self):
        response = self.client.delete(reverse('vrp-map-way-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class VrpMapWaylTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_vrp_map_way_list(self):
        response = self.client.get(reverse('vrp-map-way-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_vrp_map_way_detail(self):
        response = self.client.get(reverse('vrp-map-way-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('output_ways' in response.data)
        self.assertTrue('source_location' in response.data)

    def test_can_create_vrp_map_way(self):
        MAP_DATA = {"source_location": 1}
        response = self.client.post(reverse('vrp-map-way-list'),
                                    MAP_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_update_vrp_map_way(self):
        MAP_DATA = {"output_ways": [1]}
        response = self.client.patch(reverse('vrp-map-way-detail', args=[1]),
                                     MAP_DATA,
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_delete_vrp_map_way(self):
        response = self.client.delete(reverse('vrp-map-way-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)