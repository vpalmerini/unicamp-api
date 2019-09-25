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
        BaseAPITest.check_user_permissions(self, None, 'get',
                                           status.HTTP_200_OK, url)

    def test_get_professor_detail(self):
        """
        Anyone can make GET requests to a specific Professor
        """
        url = reverse('institute-professors-detail',
                      args=['IC', 'Pedro Rezende'])
        BaseAPITest.check_user_permissions(self, None, 'get',
                                           status.HTTP_200_OK, url)

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

    def test_delete_professor(self):
        """
        Ensure that only admins can delete Professors
        """
        url = reverse('institute-professors-detail', args=['IC', 'Pedro Rezende'])
        # non admin and unauthenticated user
        BaseAPITest.check_user_permissions(self, None, 'delete',
                                           status.HTTP_403_FORBIDDEN, url)

        # admin user
        BaseAPITest.check_user_permissions(self, 'admin', 'delete',
                                           status.HTTP_204_NO_CONTENT, url)

        # non admin and authenticated user
        BaseAPITest.check_user_permissions(self, 'user', 'delete',
                                           status.HTTP_403_FORBIDDEN, url)
