from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

#Test cases for Terms

class TermsCurrentPoint(APITestCase):

    def setUp(self):
        self.client = APIClient()
    
    def test_current_active_term_endpoint_returns_dict(self):
    
        url = reverse('api_terms_current_details', args=[1])

        # Check Anonymous User should return 403
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should return dictionary of date
        data = response.json()
        self.assertIsInstance(data, dict)