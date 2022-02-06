from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from data_api.tests.setting import username, password

from data_api.serializers import CustomerSerializer
from data_api.models import Customer


class CreateCustomerAuthenticationTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.data = {'name': 'mike'}

    def test_can_create_customer(self):
        response = self.client.post(reverse('customer-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReadCustomerAuthenticationTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name="mike")

    def test_can_read_customer_list(self):
        response = self.client.get(reverse('customer-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_read_customer_detail(self):
        response = self.client.get(
            reverse('customer-detail', args=[self.customer.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateCustomerAuthenticationTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name="mike")
        self.data = CustomerSerializer(self.customer).data
        self.data.update({'name': 'Changed'})

    def test_can_update_customer(self):
        response = self.client.put(
            reverse('customer-detail', args=[self.customer.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_update_wrong_url(self):
        response = self.client.put(reverse('customer-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteCustomerAuthenticationTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name="mike")

    def test_can_delete_customer(self):
        response = self.client.delete(
            reverse('customer-detail', args=[self.customer.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateCustomerTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)
        self.data = {'name': 'mike'}

    def test_can_create_customer(self):
        response = self.client.post(reverse('customer-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReadCustomerTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)
        self.customer = Customer.objects.create(name="mike")

    def test_can_read_customer_list(self):
        response = self.client.get(reverse('customer-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_customer_detail(self):
        response = self.client.get(
            reverse('customer-detail', args=[self.customer.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateCustomerTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)
        self.customer = Customer.objects.create(name="mike")
        self.data = CustomerSerializer(self.customer).data
        self.data.update({'name': 'Changed'})

    def test_can_update_customer(self):
        response = self.client.put(
            reverse('customer-detail', args=[self.customer.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_update_wrong_url(self):
        response = self.client.put(reverse('customer-list'), self.data)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class DeleteCustomerTest(APITestCase):

    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)
        self.customer = Customer.objects.create(name="mike")

    def test_can_delete_customer(self):
        response = self.client.delete(
            reverse('customer-detail', args=[self.customer.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
