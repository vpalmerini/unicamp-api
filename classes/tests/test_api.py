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
        BaseAPITest.check_user_permissions(self, None, 'get',
                                           status.HTTP_200_OK, url)

    def test_get_class_detail(self):
        """
        Anyone can make GET requests to a specific Class
        """
        url = reverse('institute-subject-classes-detail',
                      args=['IC', 'MC102', 'A'])
        BaseAPITest.check_user_permissions(self, None, 'get',
                                           status.HTTP_200_OK, url)

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

    def test_delete_class(self):
        """
        Ensure that only admins can delete Classes
        """
        url = reverse('institute-subject-classes-detail', args=['IC', 'MC102', 'A'])
        # non admin and unauthenticated user
        BaseAPITest.check_user_permissions(self, None, 'delete',
                                           status.HTTP_403_FORBIDDEN, url)

        # admin user
        BaseAPITest.check_user_permissions(self, 'admin', 'delete',
                                           status.HTTP_204_NO_CONTENT, url)

        # non admin and authenticated user
        BaseAPITest.check_user_permissions(self, 'user', 'delete',
                                           status.HTTP_403_FORBIDDEN, url)
