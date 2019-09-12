from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from institutes.models import Institute
from api.tests import BaseAPITest
from institutes.tests.factories import InstituteFactory


class InstituteAPITest(APITestCase):
    def setUp(self):
        InstituteFactory()
        BaseAPITest.create_admin(self)
        BaseAPITest.create_user(self)

    def test_get_institute_list(self):
        """
        Anyone can make GET requests to the list of Institutes
        """
        url = reverse('institute-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_institute_detail(self):
        """
        Anyone can make GET requests to a specific Institute
        """
        url = reverse('institute-detail', args=['IC'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_institute(self):
        """
        Ensure that only admins can create Institutes
        """
        url = reverse('institute-list')
        data = {'initials': 'IB', 'name': 'Instituto de Biologia'}
        response = self.client.post(url, data, format='json')
        # non admin and unauthenticated user
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # admin user
        self.client.login(username='admin', password='password')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # non admin user and authenticated user
        self.client.login(username='user', password='password')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_institute(self):
        """
        Ensure that only admins can edit Institutes
        """
        url = reverse('institute-detail', args=['IC'])
        data = {'initials': 'IC', 'name': 'Instituto de Comp'}
        response = self.client.put(url, data, format='json')
        # non admin and unauthenticated user
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # admin user
        self.client.login(username='admin', password='password')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # non admin and authenticated user
        self.client.login(username='user', password='password')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_institute(self):
        """
        Ensure that only admins can delete Institutes
        """
        url = reverse('institute-detail', args=['IC'])
        response = self.client.delete(url)
        # non admin and unauthenticated user
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # admin user
        self.client.login(username='admin', password='password')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # non admin and authenticated user
        self.client.login(username='user', password='password')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
