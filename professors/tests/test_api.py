from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.tests import BaseAPITest
from professors.models import Professor
from institutes.models import Institute
from classes.models import Class
from professors.tests.factories import ProfessorFactory
from classes.tests.factories import ClassFactory


class CourseAPITest(APITestCase):
    def setUp(self):
        ProfessorFactory()
        ClassFactory()
        BaseAPITest.create_admin(self)
        BaseAPITest.create_user(self)

    def test_get_professor_list(self):
        """
        Anyone can make GET requests to the list of Professors
        """
        url = reverse('institute-professors-list', args=['IC'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_professor_detail(self):
        """
        Anyone can make GET requests to a specific Professor
        """
        url = reverse('institute-professors-detail',
                      args=['IC', 'Pedro Rezende'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_professor(self):
        """
        Only admins can create Professor instances
        """
        url = reverse('institute-professors-list', args=['IC'])
        institute = Institute.objects.get()
        _class = Class.objects.get()
        data = {
            'name': 'Márcio Rosa',
            'institute': institute.initials,
            'classes': [_class.id]
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

    def test_edit_professor(self):
        """
        Only admins can edit a Professor instance
        """
        url = reverse('institute-professors-detail',
                      args=['IC', 'Pedro Rezende'])
        institute = Institute.objects.get()
        _class = Class.objects.get()
        data = {
            'name': 'Pedro Rezende a.k.a Rezende',
            'institute': institute.initials,
            'classes': [_class.id]
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

    def test_delete_professor(self):
        """
        Ensure that only admins can delete Courses
        """
        url = reverse('institute-professors-detail', args=['IC', 'Pedro Rezende'])
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
