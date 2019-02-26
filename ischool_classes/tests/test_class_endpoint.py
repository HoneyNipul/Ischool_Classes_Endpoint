from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class TestClassEndpoint(APITestCase):

    def setUp(self):
        self.client = APIClient()
    
    def test_get_should_return_listOfClass(self):
        """
        Ensure that we can see the list of classes of that term.
        """
        url = reverse('api_classes_list', args=[1])
        url = url + "?term=ab11"
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIsInstance(data, list)

    def test_get_full_information_of_particular_class(self):
        """
        Ensure we can see all the details of the particular class.
        """
        pk = '1053-71194'
        url = reverse('api_classes_detail', args=[1, pk])
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, dict)
