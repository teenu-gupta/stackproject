from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your tests here.

class FileUpload(APITestCase):
	def setUp(self):
		pass

	def testprofile(self):
		url = reverse('person_image')
		my_logo = open('/home/teenu/Pictures/29oct.png', 'r')
		token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token,HTTP_USER_AGENT='')
		response = self.client.put(url, {'logo':my_logo})
		self.assertEqual(response.status_code, status.HTTP_200_OK)