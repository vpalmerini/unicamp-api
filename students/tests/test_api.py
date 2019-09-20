from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.tests import BaseAPITest
from students.models import Student
from students.tests.factories import StudentFactory
from courses.models import Course
from classes.models import Class
from classes.tests.factories import ClassFactory


class StudentAPITest(APITestCase):
    def setUp(self):
        StudentFactory()
        ClassFactory()
        BaseAPITest.create_user(self)
        BaseAPITest.create_admin(self)

    def test_get_students_list(self):
        """
        Only authenticated or admins can get students list given a course
        """
        url = reverse('institute-course-students-list', args=['IC', 42])
        # unauthenticated user
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # authenticated user
        self.client.login(username='user', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # admin user
        self.client.login(username='admin', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_student_detail(self):
        """
        Only authenticated or admins can get students detail
        """
        url = reverse('institute-course-students-detail',
                      args=['IC', 42, '100000'])
        # unauthenticated user
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # authenticated user
        self.client.login(username='user', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # admin user
        self.client.login(username='admin', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_student(self):
        """
        Only admins can create a Student instance
        """
        url = reverse('institute-course-students-list', args=['IC', 42])
        course = Course.objects.get()
        _class = Class.objects.get()
        data = {
            'ra': '100001',
            'name': 'Raposo',
            'email': 'r100001@dac.unicamp.br',
            'course': course.id,
            'classes': [_class.class_id]
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

    def test_edit_student(self):
        """
        Only admins can edit a Student instance
        """
        url = reverse('institute-course-students-detail', args=['IC', 42, '100000'])
        course = Course.objects.get()
        _class = Class.objects.get()
        data = {
            'ra': '100000',
            'name': 'Victor Palmerini',
            'email': '200000@dac.unicamp.br',
            'course': course.id,
            'classes': [_class.class_id]
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

    def test_delete_student(self):
        """
        Only admins can delete a Student instance
        """
        url = reverse('institute-course-students-detail', args=['IC', 42, '100000'])
        response = self.client.delete(url)
        # non admin and unauthenticated user
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # admin user
        self.client.login(username='admin', password='password')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # non admin user and authenticated user
        self.client.login(username='user', password='password')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
