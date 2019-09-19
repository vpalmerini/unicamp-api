from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.tests import BaseAPITest
from subjects.models import Subject
from subjects.tests.factories import SubjectFactory
from institutes.models import Institute


class SubjectAPITest(APITestCase):
    def setUp(self):
        SubjectFactory()
        BaseAPITest.create_admin(self)
        BaseAPITest.create_user(self)

    def test_get_subject_list(self):
        """
        Anyone can make GET requests to the list of Subjects
        """
        url = reverse('institute-subjects-list', args=['IC'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_subject_detail(self):
        """
        Anyone can make GET requests to a specific Subject
        """
        url = reverse('institute-subjects-detail', args=['IC', 'MC102'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_subject(self):
        """
        Only admins can create Subject instances
        """
        url = reverse('institute-subjects-list', args=['IC'])
        institute = Institute.objects.get()
        data = {
            'initials': 'MC202',
            'name': 'Estrutura de Dados',
            'syllabus': 'Listas Ligadas e Árvores Binárias',
            'workload': 6,
            'institute': institute.initials,
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


    def test_edit_subject(self):
        """
        Only admins can edit a Subject instance
        """
        url = reverse('institute-subjects-detail',
                      args=['IC', 'MC102'])
        institute = Institute.objects.get()
        data = {
            'initials': 'MC102',
            'name': 'Programação Básica',
            'syllabus': 'Introdução a Algoritmos',
            'workload': 6,
            'institute': institute.initials,
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

    def test_delete_subject(self):
        """
        Ensure that only admins can delete Subjects
        """
        url = reverse('institute-subjects-detail', args=['IC', 'MC102'])
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
