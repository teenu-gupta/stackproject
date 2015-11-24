from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import RegisterSerializer , LoginSerializer ,\
 PersonSerializer, TokenSerializer , PassChangeSerializer , \
  EmailVerifySerializer , PersonImageSerializer , ResetPasswordConfirmSerializer , \
  ResetPasswordSerializer , SetPasswordSerializer , ConfirmEmailSerializer


from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,logout
from accounts.models import *
import datetime
import random
from accounts.events import UserRegistered , UserEmailVerify , UserResetPassword , UserEmailVerify , \
UserChangePassword

from django.contrib.auth.tokens import default_token_generator as tg
# from django.contrib.sites.models import get_current_site
from django.contrib.sites.shortcuts import get_current_site

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render_to_response
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.shortcuts import get_object_or_404
from django.http.response import Http404

# Create your views here

class Register(APIView):

	serializer_class = RegisterSerializer
	permission_classes = (permissions.AllowAny,)
	model = User

	
	def get_serializer_class(self):
		return self.serializer_class

	def post(self,request):
		# import ipdb;ipdb.set_trace()
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			
			serializer.validated_data['username'] = request.data['email']
			user=serializer.save()
			user.set_password(serializer.data['password'])
			user.save()
			token,created = Token.objects.get_or_create(user=user)
			Person(owner=user,first_name=serializer.data['first_name'],last_name=serializer.data['last_name'],email=serializer.data['email']).save()
			person = Person.objects.get(owner=user)
			PersonImage(owner=person).save()
			rr = { 
			'token': str(token),
			'first_name':user.first_name,
			'last_name':user.last_name,
			}
			return Response(rr, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		


class Login(generics.GenericAPIView):

	"""
		login a existing user to system
	"""
	serializer_class = LoginSerializer
	token_model = Token
	token_serializer = TokenSerializer

	
	def post(self,request):
		# import ipdb; ipdb.set_trace()
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			user = authenticate(username=serializer.data['username'],
								password = serializer.data['password'])

			if user and user.is_authenticated():
				if user.is_active:
					token = self.token_model.objects.get_or_create(user=user)[0].key
					return Response({'first_name':user.first_name,
									  'last_name': user.last_name,
									  'token': token
									  },status= status.HTTP_200_OK)
				else:
					return Response({'error':['Invalid Username/Password']},status = status.HTTP_401_UNAUTHORIZED)

						
			else:
				return Response({'error': ['Invalid Username/Password.']},status=status.HTTP_401_UNAUTHORIZED)
				
		else:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self,request):
		# import ipdb; ipdb.set_trace()
		try:
			logout(request)
			return Response({'sucsess':'Sucessfully Logged out.'},status= status.HTTP_200_OK)
		except Exception, e:
			print e
		return Response (status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProfileRetrieve(generics.GenericAPIView):
	"""
	Update a Profile

	"""
	model = Person
	serializer_class = PersonSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get(self,request):
		# import ipdb; ipdb.set_trace()
		person = Person.objects.get(owner=request.user.id)
		# serializer = self.serializer_class(data=request.data)
		try:
			
			serializer = PersonSerializer(person)
			return Response(data=serializer.data, status=status.HTTP_200_OK)
		except Exception,e:
			print e
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

	def put(self,request):
		# import ipdb; ipdb.set_trace()
		serializer = self.serializer_class(data=request.data)
		person = Person.objects.get(username= request.user.id)

		person.owner = request.user
		person.first_name = request.data['first_name']
		person.last_name = request.data['last_name']
		person.email= request.data['email']
		person.gender = request.data['gender']
		
		person.date_of_birth = request.data['date_of_birth'] 


		serializer= self.serializer_class(person,data=request.data)

		if serializer.is_valid():
		
			person.save()
			serializer.save()

			return Response(data=serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class ChangePassword(APIView):
    """
        Change User password to new one
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PassChangeSerializer
    model = User

    def get_serializer_class(self):
        return self.serializer_class

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if request.user.check_password(serializer.data['old_password']):
                request.user.set_password(serializer.data['new_password'])
                request.user.save()
                #request.user.auth_token.delete()
                 
                return Response({'success': 'Password successfully changed'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': ['Old password does not match']},
				status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerify(generics.GenericAPIView):
	"""
	Verify Email
	"""

	serializer_class = EmailVerifySerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		# import ipdb; ipdb.set_trace()
		if serializer.is_valid():

			try:
				user = User.objects.get(email = serializer.data['email'])
			except:
				return Response({'error':"email id does not exist exist"})
			current_site = get_current_site(request)
			site_name = current_site.name
			domain = current_site.domain
			q = UserEmailVerify()
			q.delay(ctx={'user':user,
						'email': user.email,
						'domain': domain,
						'site_name': site_name,
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'token': tg.make_token(user),
						'protocol': settings.PROTOCOL})

			return Response({'success':'Email verification mail has been sent.'})
		else:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class PersonImageView(generics.GenericAPIView):
	"""
	Add and remove person profile image
	"""

	model = PersonImage
	serializer_class = PersonImageSerializer
	permission_classes = (permissions.IsAuthenticated,)
	



	def get(self, request):
		import ipdb;ipdb.set_trace()
		profileimage = self.model.objects.get(owner__owner=request.user)
		serializer = self.serializer_class(profileimage)
		return Response(data=serializer.data, status=status.HTTP_200_OK)

	def put(self, request,format=None):
		import ipdb;ipdb.set_trace()
		profileimage = self.model.objects.get(owner__owner=request.user.id)
									
		serializer = self.serializer_class(data=request.data)	
		
		if serializer.is_valid():
			serializer.save()
			return Response(data=serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class EmailVerifyConfirm(APIView):
    """
	Email Verify Confirm
    """

    # permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, uidb64=None, token=None):
        try:
            uid = uid_decoder(uidb64)
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        person =Person.objects.get(owner=user)
        if person.is_email_verified ==True:
            return Response({'success':'Email verified successfully'},status=status.HTTP_200_OK)    
        if user is not None and tg.check_token(user, token):
            # profile = Profile.objects.get(owner=user)
            person.is_email_verified = True
            person.save()
            
            return Response({'success': 'Email verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': ['Invalid email verify token.']}, 
				status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    """
        Request Password reset
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = (permissions.AllowAny,)


    def get_serializer_class(self):
        return self.serializer_class

    def post(self, request):
    	import ipdb;ipdb.set_trace()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
            q = UserResetPassword()
            q.delay(ctx={'user':user,
                         'email': user.email,
                         'domain': domain,
                         'site_name': site_name,
                         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                         'token': tg.make_token(user),
                         'protocol': settings.PROTOCOL})
            
            return Response({'success':'Password reset e-mail has been sent.'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)



            
class ResetPasswordConfirm(APIView):
    """
        Confirm a users provided token and new password to be used
    """
    serializer_class = SetPasswordSerializer
    permission_classes = (permissions.AllowAny,)
    
    def get_serializer_class(self):
        return self.serializer_class

    def post(self, request, uidb64=None, token=None):
        # Get the UserModel
        UserModel = get_user_model()
        # Decode the uidb64 to uid to get User object
        try:
            uid = uid_decoder(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        # If we get the User object
        if user:
            serializer = self.serializer_class(data=request.data, user=user)

            if serializer.is_valid():
                person = Person.objects.get(owner=user)
                person.is_email_verified = True
                person.save()
               
                # Construct SetPasswordForm instance
                form = SetPasswordForm(user=user, data=serializer.data)

                if form.is_valid():
                    if tg.check_token(user, token):
                        form.save()

                        # Return the success message with OK HTTP status
                        return Response(
                            {"success":"Password has been reset with the new password."},
                            status=status.HTTP_200_OK)
                    else:
                        return Response(
                            {'error': ['Invalid password reset token.']},
                            status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(form._errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': ['Couldn\'t find the user from uid.']}, 
                            status=status.HTTP_400_BAD_REQUEST)

