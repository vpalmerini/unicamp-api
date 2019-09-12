from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class BaseAPITest(APITestCase):
    """
    Base class to provide repetitive functionalities
    that are used in unit tests
    """
    def create_admin(self):
        User.objects.create_user(username='admin',
                                 password='password',
                                 is_staff=True)

    def create_user(self):
        User.objects.create_user(username='user',
                                 password='password',
                                 is_staff=False)
