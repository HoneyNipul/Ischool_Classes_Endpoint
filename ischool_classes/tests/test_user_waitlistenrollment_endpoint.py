from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

# All Tests should go here!

class TermWaitListEnrollEndPoint(APITestCase):

    def setUp(self):
        self.adminclient = APIClient(enforce_csrf_checks=True)
        self.adminclient.credentials(Authorization='Bearer ' + 'regularusertoken')
        self.anonclient = APIClient(enforce_csrf_checks=True)

    def test_anonymous_user_should_get_403(self):
        url = reverse('api_my_waitlist_enroll', args=[1, '007'])

        # Check Anonymous User should return 403
        response = self.anonclient.post(url, None, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_post_should_waitlist_class_for_user(self):
        url = reverse('api_my_waitlist_enroll', args=[1, '007-876'])
 
        # Admin User
        response = self.adminclient.post(url, None, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_should_remove_user_from_waitlist(self):
        url = reverse('api_my_waitlist_enroll', args=[1, '007-876'])
 
        # Admin User
        response = self.adminclient.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
