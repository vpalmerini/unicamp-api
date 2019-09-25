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
        BaseAPITest.check_user_permissions(self, None, 'get',
                                           status.HTTP_200_OK, url)

    def test_get_institute_detail(self):
        """
        Anyone can make GET requests to a specific Institute
        """
        url = reverse('institute-detail', args=['IC'])
        BaseAPITest.check_user_permissions(self, None, 'get',
                                           status.HTTP_200_OK, url)

    def test_create_institute(self):
        """
        Ensure that only admins can create Institutes
        """
        url = reverse('institute-list')
        data = {'initials': 'IB', 'name': 'Instituto de Biologia'}
        # non admin and unauthenticated user
        BaseAPITest.check_user_permissions(self, None, 'post',
                                           status.HTTP_403_FORBIDDEN, url,
                                           data)

        # admin user
        BaseAPITest.check_user_permissions(self, 'admin', 'post',
                                           status.HTTP_201_CREATED, url, data)

        # non admin user and authenticated user
        BaseAPITest.check_user_permissions(self, 'user', 'post',
                                           status.HTTP_403_FORBIDDEN, url,
                                           data)

    def test_edit_institute(self):
        """
        Ensure that only admins can edit Institutes
        """
        url = reverse('institute-detail', args=['IC'])
        data = {'initials': 'IC', 'name': 'Instituto de Comp'}
        # non admin and unauthenticated user
        BaseAPITest.check_user_permissions(self, None, 'put',
                                           status.HTTP_403_FORBIDDEN, url,
                                           data)

        # admin user
        BaseAPITest.check_user_permissions(self, 'admin', 'put',
                                           status.HTTP_200_OK, url, data)

        # non admin and authenticated user
        BaseAPITest.check_user_permissions(self, 'user', 'put',
                                           status.HTTP_403_FORBIDDEN, url,
                                           data)

    def test_delete_institute(self):
        """
        Ensure that only admins can delete Institutes
        """
        url = reverse('institute-detail', args=['IC'])
        # non admin and unauthenticated user
        BaseAPITest.check_user_permissions(self, None, 'delete',
                                           status.HTTP_403_FORBIDDEN, url)

        # admin user
        BaseAPITest.check_user_permissions(self, 'admin', 'delete',
                                           status.HTTP_204_NO_CONTENT, url)

        # non admin and authenticated user
        BaseAPITest.check_user_permissions(self, 'user', 'delete',
                                           status.HTTP_403_FORBIDDEN, url)
