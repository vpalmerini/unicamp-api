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
        BaseAPITest.check_user_permissions(self, None, 'get',
                                           status.HTTP_200_OK, url)

    def test_get_subject_detail(self):
        """
        Anyone can make GET requests to a specific Subject
        """
        url = reverse('institute-subjects-detail', args=['IC', 'MC102'])
        BaseAPITest.check_user_permissions(self, None, 'get',
                                           status.HTTP_200_OK, url)

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

    def test_delete_subject(self):
        """
        Ensure that only admins can delete Subjects
        """
        url = reverse('institute-subjects-detail', args=['IC', 'MC102'])
        # non admin and unauthenticated user
        BaseAPITest.check_user_permissions(self, None, 'delete',
                                           status.HTTP_403_FORBIDDEN, url)

        # admin user
        BaseAPITest.check_user_permissions(self, 'admin', 'delete',
                                           status.HTTP_204_NO_CONTENT, url)

        # non admin and authenticated user
        BaseAPITest.check_user_permissions(self, 'user', 'delete',
                                           status.HTTP_403_FORBIDDEN, url)
