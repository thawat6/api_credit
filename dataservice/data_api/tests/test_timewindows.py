from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class TimeWindowAuthenticationTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/time-windows/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_time_window_list(self):
        response = self.client.get(reverse('time-window-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_read_time_window_detail(self):
        response = self.client.get(reverse('time-window-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('id' in response.data)
        self.assertFalse('begin' in response.data)
        self.assertFalse('end' in response.data)

    def test_can_delete_time_window(self):
        response = self.client.delete(reverse('time-window-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_time_window(self):
        TW_DATA = {"begin": "08:00:00", "end": "15:00:00"}

        response = self.client.post(reverse('time-window-list'),
                                    TW_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_time_window(self):
        TW_DATA = {"begin": "09:00:00", "end": "18:00:00"}
        response = self.client.put(reverse('time-window-detail', args=[1]),
                                   TW_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TimeWindowTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/time-windows/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_time_window_list(self):
        response = self.client.get(reverse('time-window-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_time_window_detail(self):
        response = self.client.get(reverse('time-window-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('begin' in response.data)
        self.assertTrue('end' in response.data)

    def test_can_delete_time_window(self):
        response = self.client.delete(reverse('time-window-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_create_time_window(self):
        TW_DATA = {"begin": "08:00:00", "end": "15:00:00"}

        response = self.client.post(reverse('time-window-list'),
                                    TW_DATA,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_update_time_window(self):
        TW_DATA = {"begin": "09:00:00", "end": "18:00:00"}
        response = self.client.put(reverse('time-window-detail', args=[1]),
                                   TW_DATA,
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
