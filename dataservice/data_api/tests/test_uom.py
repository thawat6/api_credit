from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from data_api.tests.setting import username, password


class UnitOfMeasureAuthenticationTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/unit-of-measures/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_uom_list(self):
        response = self.client.get(reverse('unit-of-measure-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_read_uom_detail(self):
        response = self.client.get(
            reverse('unit-of-measure-detail', args=['1']))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('id' in response.data)
        self.assertFalse('name' in response.data)
        self.assertFalse('rounding' in response.data)
        self.assertFalse('factor' in response.data)

    def test_can_read_uom_detail_by_name(self):
        response = self.client.get(
            reverse('unit-of-measure-detail', args=['pcs']))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('id' in response.data)
        self.assertFalse('name' in response.data)
        self.assertFalse('rounding' in response.data)
        self.assertFalse('factor' in response.data)

    def test_can_not_delete_uom(self):
        response = self.client.delete(
            reverse('unit-of-measure-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UnitOfMeasureCategoryAuthenticationTest(APITestCase):
    '''
    Test get game detail information can be shown
    GET /vrp/api/unit-of-measure-categories/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()

    def test_can_read_uom_cat_list(self):
        response = self.client.get(reverse('unit-of-measure-categories-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('count' in response.data)
        self.assertFalse('results' in response.data)

    def test_can_read_uom_cat_detail(self):
        response = self.client.get(
            reverse('unit-of-measure-categories-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('id' in response.data)
        self.assertFalse('name' in response.data)

    def test_can_not_delete_uom_cat(self):
        response = self.client.delete(
            reverse('unit-of-measure-categories-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UnitOfMeasureTest(APITestCase):
    '''
    Test get game detail information can be shown
    [GET] /vrp/api/unit-of-measures/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_uom_list(self):
        response = self.client.get(reverse('unit-of-measure-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_uom_detail(self):
        response = self.client.get(
            reverse('unit-of-measure-detail-by-name', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('category' in response.data)
        self.assertTrue('name' in response.data)
        self.assertTrue('rounding' in response.data)
        self.assertTrue('factor' in response.data)

    def test_can_update_uom(self):
        UOM_DATA = {
            "name": "pcs update",
            "uom_type": "smaller",
            "category": 2,
            "rounding": 1,
            "factor": 2.0
        }
        response = self.client.patch(reverse('unit-of-measure-detail-by-name',
                                             args=[1]),
                                     UOM_DATA,
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_uom_detail_not_found(self):
        response = self.client.get(
            reverse('unit-of-measure-detail-by-name', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_read_uom_detail_by_name(self):
        response = self.client.get(
            reverse('unit-of-measure-detail-by-name', args=['pcs']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('name' in response.data)
        self.assertTrue('rounding' in response.data)
        self.assertTrue('factor' in response.data)

    def test_can_delete_uom(self):
        response = self.client.delete(
            reverse('unit-of-measure-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UnitOfMeasureCategoryTest(APITestCase):
    '''
    Test get game detail information can be shown
    GET /vrp/api/unit-of-measure-categories/
    '''
    fixtures = ['auth.json', 'data_api.json']

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=username, password=password)

    def test_can_read_uom_cat_list(self):
        response = self.client.get(reverse('unit-of-measure-categories-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('count' in response.data)
        self.assertTrue('results' in response.data)

    def test_can_read_uom_cat_detail(self):
        response = self.client.get(
            reverse('unit-of-measure-categories-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertTrue('name' in response.data)

    def test_can_not_delete_uom_cat(self):
        response = self.client.delete(
            reverse('unit-of-measure-categories-detail', args=[1]))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_can_read_uom_cat_not_found(self):
        response = self.client.get(
            reverse('unit-of-measure-categories-detail', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)