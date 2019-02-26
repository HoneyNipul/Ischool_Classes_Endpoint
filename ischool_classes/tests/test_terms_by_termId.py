from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

#Test cases for Terms

class TermsByTermIdEndPoint(APITestCase):

    def setUp(self):
        self.client = APIClient()
    
    def test_terms_schedule_endpoint_return_valid_term(self):
        termId=1183
        url = reverse('api_terms_by_termId', args=[1,termId])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIsNotNone(data["termId"])

    def test_terms_schedule_endpoint_return_404(self):
        """ Shoud return a 404 when not found
        """
        termId=9999
        url = reverse('api_terms_by_termId', args=[1,termId])
        response = self.client.get(url, format='json')
        
        # This should be 404, but the current ischool api does not return the proper code
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)