from django.conf.urls import include , url
from django.contrib import admin
from stackapp import views

urlpatterns = [
	url(r'^questions/$',views.QuestionPost.as_view(), name ='questionpost'),
	url(r'^answers/$',views.AnswerPost.as_view(),name='answerpost'),
	url(r'^questionlist/$',views.QuestionDetail.as_view(),name ='questiondetail'),
	url(r'^answerlist/$',views.AnswerDetail.as_view(),name='answerlist'),
	url(r'^questionupdate/(?P<pk>[0-9]+)/$',views.QuestionUpdate.as_view(),name='questiondelete'),
	url(r'^answerupdate/(?P<pk>[0-9]+)/$',views.AnswerUpdate.as_view(),name='answerupdate'),
	url(r'^userdashboard/$',views.UserDashboard.as_view(),name= 'userdashboard'),

	url(r'^questanslist/(?P<pk>[0-9]+)/$',views.QuestionAnswerList.as_view(),name='quesanslist'),
	url(r'^votequestion/$',views.VotingQuestionAnswer.as_view(), name= 'votequesans'),
	#url(r'^ratingques/$',views.RatingQuesAns.as_view(),name='ratingques'),
	url(r'^votesquestion/$',views.VotesQuesAnswerList.as_view(),name='votesques'),
	#url(r'^votesquestioncount/(?P<pk>[0-9]+)/$',views.VotesQuestionDetails.as_view(),name='votesquestioncount'),
	#answer apis
	
	url(r'^hashtag/$',views.HashTagCreation.as_view(),name='hashtagview'),
	url(r'^hashtaglist/$',views.HashTagDetails.as_view(),name='hashtaglist'),

] 


