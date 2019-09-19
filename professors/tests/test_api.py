from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.tests import BaseAPITest
from professors.models import Professor
from institutes.models import Institute
from professors.tests.factories import ProfessorFactory


class CourseAPITest(APITestCase):
    def setUp(self):
        ProfessorFactory()
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
