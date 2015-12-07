from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# from accounts.models import Person

# Create your models here.

class Hashtags(models.Model):
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=200)

	def __unicode__(self):
		return self.title


class Question(models.Model):
	CHOICE_STATUS = (("raised",_("Raised")),("posted",_("Posted")),("answered",_("Answered")),("irrelevant",_("Irrelevant")))
	title = models.CharField(max_length=200)
	asked_by = models.ForeignKey(User)
	created_date = models.DateField(auto_now=True)
	hashtag = models.ManyToManyField(Hashtags,blank=True)
	status = models.CharField(max_length=200,choices=CHOICE_STATUS,blank=True,null=True,default=CHOICE_STATUS[0][0])

	def __unicode__(self):
		return self.title

class Answer(models.Model):
	title = models.CharField(max_length=200)
	answered_by = models.ForeignKey(User, related_name = 'answered_by')
	question = models.ForeignKey(Question,related_name = 'answer_of')
	created_date = models.DateField(auto_now= True)

	def __unicode__(self):
		return self.title


class Vote(models.Model):

	CURRENT_STATUS = ((0,'Downvote'),(1,'Upvote'))
	vote_type = models.SmallIntegerField(choices=CURRENT_STATUS, blank = True, default = True)
	voted_by = models.ForeignKey(User)
	question = models.ForeignKey(Question,null=True)
	answer = models.ForeignKey(Answer,null = True)


	def __unicode__(self):
		return str(self.voted_by)







	



	




