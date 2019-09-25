from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.tests import BaseAPITest
from courses.models import Course
from institutes.models import Institute
from courses.tests.factories import CourseFactory


class CourseAPITest(APITestCase):
    def setUp(self):
        CourseFactory()
        BaseAPITest.create_admin(self)
        BaseAPITest.create_user(self)

    def test_get_course_list(self):
        """
        Anyone can make GET requests to the list of Courses
        """
        url = reverse('institute-courses-list', args=['IC'])
        BaseAPITest.check_user_permissions(self, None, 'get',
                                           status.HTTP_200_OK, url)

    def test_get_course_detail(self):
        """
        Anyone can make GET requests to a specific Course
        """
        url = reverse('institute-courses-detail', args=['IC', 42])
        BaseAPITest.check_user_permissions(self, None, 'get',
                                           status.HTTP_200_OK, url)

    def test_create_course(self):
        """
        Ensure that only admins can create Courses
        """
        url = reverse('institute-courses-list', args=['IC'])
        institute = Institute.objects.get()
        data = {
            'id': 12,
            'name': 'Engenharia Civil',
            'shift': 'Integral',
            'institute': institute.initials
        }
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

    def test_edit_course(self):
        """
        Ensure that only admins can edit Courses
        """
        url = reverse('institute-courses-detail', args=['IC', 42])
        institute = Institute.objects.get()
        data = {
            'id': 12,
            'name': 'Engenharia CivilTerrorista',
            'shift': 'Integral',
            'institute': institute.initials
        }
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

    def test_delete_course(self):
        """
        Ensure that only admins can delete Courses
        """
        url = reverse('institute-courses-detail', args=['IC', 42])
        # non admin and unauthenticated user
        BaseAPITest.check_user_permissions(self, None, 'delete',
                                           status.HTTP_403_FORBIDDEN, url)

        # admin user
        BaseAPITest.check_user_permissions(self, 'admin', 'delete',
                                           status.HTTP_204_NO_CONTENT, url)

        # non admin and authenticated user
        BaseAPITest.check_user_permissions(self, 'user', 'delete',
                                           status.HTTP_403_FORBIDDEN, url)
