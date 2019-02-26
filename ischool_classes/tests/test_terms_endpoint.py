from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

#Test cases

class TermEndPoint(APITestCase):

    def setUp(self):
        self.client = APIClient()
    
    def test_term_endpoint(self):
        

        url = reverse('api_terms_list', args=[1])

        # Check Anonymous User should return 403
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
        data = response.json()
        self.assertIsInstance(data,list)
        # Admin User
        #self.client.credentials(Authorization='Bearer ' + 'adminusertoken')
        #response = self.client.get(url, format='json')
       # self.assertEqual(response.status_code, status.HTTP_200_OK)