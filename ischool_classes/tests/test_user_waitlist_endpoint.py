from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

# All Tests should go here!

class TestUserWaitlistEndpoint(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_anonymous_user_should_return_403(self):
        url = reverse('api_my_waitlist', args=[1])

        # Check Anonymous User should return 403
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_authenticated_user_get_should_return_list_of_classes(self):
        """
        Ensure that we can see the waitlisted class of the user.
        """
        url = reverse('api_my_waitlist', args=[1])
 
        # Admin User
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = response.json()

        self.assertIsInstance(response_data, list)

    def test_active_waitlist_terms(self):
        
        url = reverse('api_terms_active_waitlist_terms', args=[1])

        # Admin User
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = response.json()

        self.assertIsInstance(response_data, list)