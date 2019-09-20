from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.tests import BaseAPITest
from classes.models import Class
from classes.tests.factories import ClassFactory
from subjects.models import Subject
from courses.models import Course
from courses.tests.factories import CourseFactory


class ClassAPITest(APITestCase):
    def setUp(self):
        ClassFactory()
        CourseFactory()
        BaseAPITest.create_admin(self)
        BaseAPITest.create_user(self)

    def test_get_classes_list(self):
        """
        Anyone can make GET requests to the list of Classes
        """
        url = reverse('institute-subject-classes-list', args=['IC', 'MC102'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_class_detail(self):
        """
        Anyone can make GET requests to a specific Class
        """
        url = reverse('institute-subject-classes-detail',
                      args=['IC', 'MC102', 'A'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_class(self):
        """
        Only admins can create Class instances
        """
        url = reverse('institute-subject-classes-list', args=['IC', 'MC102'])
        subject = Subject.objects.get()
        course = Course.objects.get()
        data = {
            'class_id': 'A',
            'positions': 30,
            'enrolled': 28,
            'subject': subject.initials,
            'course_reservation': [course.id]
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

    def test_edit_class(self):
        """
        Only admins can edit Class instances
        """
        url = reverse('institute-subject-classes-detail', args=['IC', 'MC102', 'A'])
        subject = Subject.objects.get()
        course = Course.objects.get()
        data = {
            'class_id': 'B',
            'positions': 30,
            'enrolled': 28,
            'subject': subject.initials,
            'course_reservation': [course.id]
        }
        response = self.client.put(url, data, format='json')
        # non admin and unauthenticated user
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # admin user
        self.client.login(username='admin', password='password')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # non admin user and authenticated user
        self.client.login(username='user', password='password')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_class(self):
        """
        Ensure that only admins can delete Classes
        """
        url = reverse('institute-subject-classes-detail', args=['IC', 'MC102', 'A'])
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
