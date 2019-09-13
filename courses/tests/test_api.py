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
        url = reverse('courses-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_course_detail(self):
        """
        Anyone can make GET requests to a specific Course
        """
        url = reverse('courses-detail', args=[42])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course(self):
        """
        Ensure that only admins can create Courses
        """
        url = reverse('courses-list')
        institute = Institute.objects.get()
        data = {
            'id': 12,
            'name': 'Engenharia Civil',
            'shift': 'Integral',
            'institute': institute.initials
        }
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

    def test_edit_course(self):
        """
        Ensure that only admins can edit Courses
        """
        url = reverse('courses-detail', args=[42])
        institute = Institute.objects.get()
        data = {
            'id': 12,
            'name': 'Engenharia CivilTerrorista',
            'shift': 'Integral',
            'institute': institute.initials
        }
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

    def test_delete_course(self):
        """
        Ensure that only admins can delete Courses
        """
        url = reverse('courses-detail', args=[42])
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
