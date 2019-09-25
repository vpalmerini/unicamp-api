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
        BaseAPITest.check_user_permissions(self, None, 'get',
                                           status.HTTP_403_FORBIDDEN, url)
        # authenticated user
        BaseAPITest.check_user_permissions(self, 'user', 'get',
                                           status.HTTP_200_OK, url)
        # admin user
        BaseAPITest.check_user_permissions(self, 'admin', 'get',
                                           status.HTTP_200_OK, url)

    def test_get_student_detail(self):
        """
        Only authenticated or admins can get students detail
        """
        url = reverse('institute-course-students-detail',
                      args=['IC', 42, '100000'])
        # unauthenticated user
        BaseAPITest.check_user_permissions(self, None, 'get',
                                           status.HTTP_403_FORBIDDEN, url)
        # authenticated user
        BaseAPITest.check_user_permissions(self, 'user', 'get',
                                           status.HTTP_200_OK, url)
        # admin user
        BaseAPITest.check_user_permissions(self, 'admin', 'get',
                                           status.HTTP_200_OK, url)

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

    def test_edit_student(self):
        """
        Only admins can edit a Student instance
        """
        url = reverse('institute-course-students-detail',
                      args=['IC', 42, '100000'])
        course = Course.objects.get()
        _class = Class.objects.get()
        data = {
            'ra': '100000',
            'name': 'Victor Palmerini',
            'email': '200000@dac.unicamp.br',
            'course': course.id,
            'classes': [_class.class_id]
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

    def test_delete_student(self):
        """
        Only admins can delete a Student instance
        """
        url = reverse('institute-course-students-detail',
                      args=['IC', 42, '100000'])
        # non admin and unauthenticated user
        BaseAPITest.check_user_permissions(self, None, 'delete',
                                           status.HTTP_403_FORBIDDEN, url)

        # admin user
        BaseAPITest.check_user_permissions(self, 'admin', 'delete',
                                           status.HTTP_204_NO_CONTENT, url)

        # non admin and authenticated user
        BaseAPITest.check_user_permissions(self, 'user', 'delete',
                                           status.HTTP_403_FORBIDDEN, url)
