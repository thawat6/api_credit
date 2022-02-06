from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class CoordAuthenticationTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/coords/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_coord_list(self):
        response = self.client.get(reverse('coord-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_read_coord_detail(self):
        response = self.client.get(reverse('coord-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('id' in response.data)
        self.assertFalse('lat' in response.data)
        self.assertFalse('lon' in response.data)

    def test_can_delete_coord(self):
        response = self.client.delete(reverse('coord-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_coord(self):
        COORD_DATA = {"lat": "16.431540", "lon": "102.836880"}

        response = self.client.post(reverse('coord-list'),
                                    COORD_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_coord(self):
        COORD_DATA = {"lat": "16.400000", "lon": "103.836880"}
        response = self.client.put(reverse('coord-detail', args=[1]),
                                   COORD_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CoordTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/coords/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_coord_list(self):
        response = self.client.get(reverse('coord-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_coord_detail(self):
        response = self.client.get(reverse('coord-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('lat' in response.data)
        self.assertTrue('lon' in response.data)

    def test_can_delete_coord(self):
        response = self.client.delete(reverse('coord-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_create_coord(self):
        COORD_DATA = {"lat": "16.431540", "lon": "102.836880"}

        response = self.client.post(reverse('coord-list'),
                                    COORD_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_update_coord(self):
        COORD_DATA = {"lat": "16.400000", "lon": "103.836880"}
        response = self.client.put(reverse('coord-detail', args=[1]),
                                   COORD_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
