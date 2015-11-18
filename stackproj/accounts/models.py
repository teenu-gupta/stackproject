from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
import urllib, mimetypes
from django.core.validators import MinLengthValidator


User.REQUIRED_FIELDS = ['username']
User.USERNAME_FIELD = "email"
User._meta.get_field_by_name('email')[0]._unique = True

def profile_image_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = 'user_id_' + str(instance.owner.id) + '.' + ext
	return '/'.join(['person/profile-image', str(instance.owner.id), filename])




class Person(models.Model):
	CURRENT_STATUS = ((0,'Male'),(1,'Female'))

	owner = models.OneToOneField(User,related_name='profile')
	email = models.EmailField()
	gender = models.SmallIntegerField(choices=CURRENT_STATUS, blank = True, default = True)
	date_of_birth = models.DateField(_("Date"),null=True,blank=True)

	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	is_email_verified   = models.BooleanField(_('Email Verified'), default=False)
	last_login = models.DateTimeField(_('last login'), default=timezone.now)
	

	def __unicode__(self):
		return str(self.owner)



	# #property to calculate the points
	# @property
	#    def user_score(self):
	#        if self.current_status == 0:
	#            return False
	#        else:
	#            return True
    

class PersonImage(models.Model):
	owner = models.OneToOneField(Person, unique=True, related_name='profile_image')
	# image = models.ImageField(upload_to=profile_image_path, blank=True, null=True)
	image = models.ImageField(upload_to=profile_image_path, blank=True, null=True)



