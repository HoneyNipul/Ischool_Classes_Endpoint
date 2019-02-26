from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

#Test cases for Terms

class TermsScheduleEndPoint(APITestCase):

    def setUp(self):
        self.client = APIClient()
    
    def test_current_active_terms_view_returns_list(self):
        

        url = reverse('api_terms_schedule_list', args=[1])

        # Check Anonymous User should return 403
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
        data = response.json()
        self.assertIsInstance(data,list)