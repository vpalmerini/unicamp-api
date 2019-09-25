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

    def check_user_permissions(self, user, method, status, url, *args):
        """
        Log an user or admin and test if has the necessary permission
        """
        if (user):
            self.client.login(username=user, password='password')

        if (method == 'get'):
            response = self.client.get(url, format='json')
        elif (method == 'post'):
            response = self.client.post(url, args[0], format='json')
        elif (method == 'put'):
            response = self.client.put(url, args[0], format='json')
        elif (method == 'delete'):
            response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status)
