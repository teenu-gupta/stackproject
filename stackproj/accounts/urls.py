from accounts import views
from django.conf.urls import patterns, url


urlpatterns = patterns('',
	url(r'^register/$',views.Register.as_view(), name= 'register'),
	url(r'^login/$',views.Login.as_view(), name = 'login'),
	url(r'^logout/$',views.Logout.as_view(),name='logout'),
	url(r'^profile/$',views.ProfileRetrieve.as_view(), name='profileupdate'),
	url(r'^change_password/$', views.ChangePassword.as_view(), name='change_password'),

	url(r'^verify_email/$', views.EmailVerify.as_view(), name='verify_email'),
	url(r'^verify_email_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
	views.EmailVerifyConfirm.as_view(), name='verify_email_confirm'),

	url(r'^person-image/$', views.PersonImageView.as_view(), name='person_image'),
	
	url(r'^password_reset/$', views.ResetPassword.as_view(), name='password_reset'),
	url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
	views.ResetPasswordConfirm.as_view(), name='password_reset_confirm'),
	)




