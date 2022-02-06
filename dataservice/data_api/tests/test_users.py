from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from data_api.tests.setting import username, password

from data_api.serializers import UserSerializer
from data_api.models import User


class CreateUserAuthenticationTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.data = {
            'first_name': 'mike',
            'last_name': 'mike',
            'username': 'mike'
        }

    def test_can_create_user(self):
        response = self.client.post(reverse('user-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReadUserAuthenticationTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(first_name="mike",
                                        last_name="mike",
                                        username="mike")

    def test_can_read_user_list(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_read_user_detail(self):
        response = self.client.get(reverse('user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateUserAuthenticationTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(first_name="mike",
                                        last_name="mike",
                                        username="mike")
        self.data = UserSerializer(self.user).data
        self.data.update({'first_name': 'golf'})

    def test_can_update_user(self):
        response = self.client.put(reverse('user-detail', args=[self.user.id]),
                                   self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_update_wrong_url(self):
        response = self.client.put(reverse('user-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteUserAuthenticationTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(first_name="mike",
                                        last_name="mike",
                                        username="mike")

    def test_can_delete_user(self):
        response = self.client.delete(
            reverse('user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateUserTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)
        self.data = {
            'first_name': 'mike',
            'last_name': 'mike',
            'username': 'mike',
            'password': '12345678',
            'confirm_password': '12345678',
            'role': 'back_officer'
        }

    def test_can_create_user(self):
        response = self.client.post(reverse('user-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReadUserTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)
        self.user = User.objects.create(first_name="mike",
                                        last_name="mike",
                                        username="mike")

    def test_can_read_user_list(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_user_detail(self):
        response = self.client.get(reverse('user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateUserTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)
        self.data = {
            'first_name': 'mike',
            'last_name': 'golf',
            'username': 'mikegolf',
            'password': '12345678',
            'confirm_password': '12345678',
            'role': 'back_officer'
        }

    def test_can_update_user(self):
        response = self.client.put(reverse('user-detail', args=[1]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_partial_update_user(self):
        partial_data = {'first_name': 'new_mike', 'last_name': 'new_golf'}
        response = self.client.patch(reverse('user-detail', args=[1]),
                                     partial_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_update_wrong_url(self):
        response = self.client.put(reverse('user-list'), self.data)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class UpdateUserPasswordTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)
        self.data = {
            'first_name': 'mike',
            'last_name': 'golf',
            'username': 'mikegolf',
            'password': '12345678',
            'confirm_password': '12345678',
            'role': 'back_officer'
        }

    def test_can_update_user_password(self):
        partial_data = {"password": "1q2w3e4r", "confirm_password": "1q2w3e4r"}
        response = self.client.patch(reverse('set-password', args=[1]),
                                     partial_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()
        self.client.login(username=username, password="1q2w3e4r")
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_update_user_password_not_match(self):
        partial_data = {"password": "1q2w3e4r", "confirm_password": "1Q2W3E4R"}
        response = self.client.patch(reverse('set-password', args=[1]),
                                     partial_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
        self.client.login(username=username, password="1Q2W3E4R")
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_user_no_found(self):
        partial_data = {"password": "1q2w3e4r", "confirm_password": "1q2w3e4r"}
        response = self.client.patch(reverse('set-password', args=[99]),
                                     partial_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_can_update_user_password_not_string(self):
    #     partial_data = {"password": 000, "confirm_password": 000}
    #     response = self.client.patch(reverse('set-password', args=[1]), partial_data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteUserTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_delete_user(self):
        response = self.client.delete(reverse('user-detail', args=[2]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
