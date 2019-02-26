from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class ClassWaitlistViewSetTestCase(APITestCase):

    def setUp(self):
        self.reg_user_client = APIClient(HTTP_AUTHORIZATION="Bearer regularusertoken")
        self.client = APIClient()

    def test_anon_user_should_get_a_403(self):
        url = reverse('api_class_waitlist', args=[1, '1192'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_instructor_of_class_should_get_a_list_of_students_enrolled(self):
        url = reverse('api_class_waitlist', args=[1, '1192'])
        response = self.reg_user_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)


    
