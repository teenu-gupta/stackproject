from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator as tg
from rest_framework.authtoken.models import Token
from django.core.validators import MinLengthValidator
from rest_framework import serializers
from accounts.models import *

import re
from django.contrib.auth.models import User

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class PersonImageSerializer(serializers.ModelSerializer):
	# image = Base64ImageField(max_length=None, use_url=True)


	class Meta:
		model = PersonImage
		fields = ('image',)



class RegisterSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('first_name','last_name','password','email')
		write_only_fields = ('password',)
		# extra_kwargs = {'password': {'write_only': True}}


		# def create(self, validated_data):
		# 	user = User(
		# 	email=validated_data['email'],
		# 	username=validated_data['username'],
		# 	first_name = validated_data['first_name'],
		# 	last_name = validated_data['last_name'],
		# 	)
		# 	user.set_password(validated_data['password'])
		# 	user.save()
		# 	return users

class LoginSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=100)
	password = serializers.CharField(validators=[MinLengthValidator(6)])
	class Meta:
		model = User
	

	
class TokenSerializer(serializers.Serializer):
	class Meta:
		model = Token
		fields = ('key',)
				

class PersonSerializer(serializers.ModelSerializer):
	profile_image = PersonImageSerializer()
	class Meta:
		model = Person
		fields = ('email','gender','date_of_birth','first_name' , 'last_name','profile_image')
		read_only_fields = ('owner','profile_image')

		




class PassChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[MinLengthValidator(6)])

    def validate(self, attrs):
        old_password = attrs['old_password']
        new_password = attrs['new_password']
        if old_password == new_password:
            raise serializers.ValidationError('old and new password are same')
        return attrs



class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()

    # def validate_email(self, attrs):
    #     email = attrs['email'].lower()
    #     if email and Person.objects.filter(owner__email=email, is_email_verified=True).count():
    #         raise serializers.ValidationError("Email already verified")
    #     return attrs

class ConfirmEmailSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=256)

    def validate(self, attrs):
        token = attrs['token']
        rg = re.match(r'(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})', token)  # @IgnorePep8
        if rg:
            uidb64, eml_token = rg.groups()
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User._default_manager.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user is not None and tg.check_token(user, token):
                user.verified = True
                user.save()
                return attrs
        else:
            serializers.ValidationError('Invalid token')


class SetPasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(validators=[MinLengthValidator(6)])
    new_password2 = serializers.CharField(validators=[MinLengthValidator(6)])

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        return super(SetPasswordSerializer, self).__init__(*args, **kwargs)
    
    def validate(self, attrs):
        new_password1 = attrs['new_password1']
        new_password2 = attrs['new_password2']
        if new_password1 != new_password2:
            raise serializers.ValidationError('Passwords are not same.')
        return attrs



class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    #to do 

    # def validate_email(self, args):
    #     email = args['email']
    #     try:
    #         usr = User.objects.get(email=email)
    #     except User.DoesNotExist:
    #         raise serializers.ValidationError('No user with this email'
    #                                           ' registered'
    #                                           )
    #     except User.MultipleRowsReturned:
    #         raise serializers.ValidationError('Multiple Accounts'
    #                                           ' same email found')
    #     if not usr.is_active:
    #         raise serializers.ValidationError('User account is'
    #                                           ' disabled')
    #     args['user'] = usr
    #     return args

        
class ResetPasswordConfirmSerializer(serializers.Serializer):

    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True,
                                     validators=[MinLengthValidator(6)])

    class Meta:
        model = User
        fields = ('token', 'password')
        write_only_fields = ('password',)

    def validate(self, attrs):
        token = attrs['token']
        rg = re.match(r'(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})', token)  # @IgnorePep8
        if rg:
            uidb64, eml_token = rg.groups()
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User._default_manager.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user is not None and tg.check_token(user, eml_token):
                attrs['user'] = user
                return attrs
        raise serializers.ValidationError('Invalid token')


