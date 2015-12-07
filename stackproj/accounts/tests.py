from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from accounts.models import Person , PersonImage


class RegisterTestCase(APITestCase):
	def setUp(self):
		self.em_visitor = 'visitor@gmail.com'
		self.pw_visitor = 'visitor'
		self.first_name = 'tanu'
		self.last_name = 'gupta'

		self.em_user = 'user@gmail.com'
		self.pw_user = 'userpass'
		user = get_user_model().objects.create(first_name = self.first_name,last_name=self.last_name,email=self.em_user,password = self.pw_user,username= self.em_user)
		profile = Person.objects.create(owner=user,is_email_verified=True)

	def test_registration(self):
		url = reverse('register')
		data_dicts = {
						'first_name':'tanu',
						'last_name': 'gupta',
						'email':'tanu@dispostable.com',
						'password':'test1234',
						

		}

		response = self.client.post(url,data_dicts)
		user = get_user_model().objects.latest('id')
		self.assertEqual(user.email,data_dicts['email'])
		self.assertEqual(response.status_code,status.HTTP_200_OK)

class LoginTestCase(APITestCase):
	def setUp(self):
		pass

	def test_login_incorrect(self):
		url = reverse('login')
		error_dict = {
						'info':{'username':'XXX','password':'qwerty'},
						'status_code': status.HTTP_401_UNAUTHORIZED,
		}

		response = self.client.post(url,error_dict['info'])
		self.assertEqual(response.status_code,error_dict['status_code'])

	def test_login_correct(self):
		url_register = reverse('register')
		payload_register = {
						'first_name':'tanu',
						'last_name': 'gupta',
						'email':'tanu@dispostable.com',
						'password':'test1234',
		}
		response_register = self.client.post(url_register,payload_register)

		url = reverse('login')
		error_dict = {
						'info':{'username':'tanu@dispostable.com','password':'test1234'},
						'status_code':status.HTTP_200_OK,

		}
		response = self.client.post(url,error_dict['info'])
		self.assertEqual(response.status_code,error_dict['status_code'])
		self.assertIn('token',response.data)
		token = response.data['token']
		# self.client.credentials(HTTP_AUTHORIZATION='Token ' + token,HTTP_USER_AGENT='')
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
		url_logout = reverse('logout')
		response_logout = self.client.get(url_logout)
		# import ipdb;ipdb.set_trace()
		self.assertEqual(response_logout.data['success'],'Sucessfully Logged out.')
		self.assertEqual(response_logout.status_text,'Unauthorized')
		self.assertEqual(response_logout.status_code,status.HTTP_200_OK)

	# def test_login_failure(self):








