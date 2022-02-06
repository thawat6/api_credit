from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class VrpMapOutWayAuthenticationTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/maps/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_vrp_map_out_way_list(self):
        response = self.client.get(reverse('vrp-map-out-way-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_read_vrp_map_out_way_detail(self):
        response = self.client.get(reverse('vrp-map-out-way-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_vrp_map_out_way(self):
        MAP_DATA = {
            "output_location": 1,
            "duration": "10:10:10",
            "distance": 1,
            "distance_uom": 1
        }
        response = self.client.post(reverse('vrp-map-out-way-list'),
                                    MAP_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_vrp_map_out_way(self):
        MAP_DATA = {
            "output_location": 2,
            "duration": "00:07:00",
            "distance": 1.9,
            "distance_uom": 4
        }
        response = self.client.patch(reverse('vrp-map-out-way-detail',
                                             args=[1]),
                                     MAP_DATA,
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_delete_vrp_map_out_way(self):
        response = self.client.delete(
            reverse('vrp-map-out-way-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class VrpMapOutWayTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/maps/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_vrp_map_out_way_list(self):
        response = self.client.get(reverse('vrp-map-out-way-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_vrp_map_out_way_detail(self):
        response = self.client.get(reverse('vrp-map-out-way-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('distance' in response.data)
        self.assertTrue('duration' in response.data)
        self.assertTrue('output_location' in response.data)

    def test_can_create_vrp_map_out_way(self):
        MAP_DATA = {
            "output_location": 1,
            "duration": "10:10:10",
            "distance": 1,
            "distance_uom": 1
        }
        response = self.client.post(reverse('vrp-map-out-way-list'),
                                    MAP_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_update_vrp_map_out_way(self):
        MAP_DATA = {
            "output_location": 2,
            "duration": "00:07:00",
            "distance": 1.9,
            "distance_uom": 4
        }
        response = self.client.patch(reverse('vrp-map-out-way-detail',
                                             args=[1]),
                                     MAP_DATA,
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_delete_vrp_map_out_way(self):
        response = self.client.delete(
            reverse('vrp-map-out-way-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
