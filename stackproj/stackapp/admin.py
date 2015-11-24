from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from  stackapp.models import Question, Answer , Vote , Hashtags
from stackapp.resources import QuestionResource , AnswerResource
from datetime import datetime , timedelta
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# admin.site.disable_action('delete_selected')

class AnswerAdmin(ImportExportModelAdmin):
	
	resource_class = AnswerResource

class AnswerAdminInline(admin.TabularInline):
	model = Answer
	fk_name = 'question'
	readonly_fields = ('title','answered_by','created_date')
	actions = None
	

	def has_add_permission(self,request):
		return False


class QuestionAdmin(ImportExportModelAdmin):

	# list_display = ('id','title','asked_by','created_date','question_owner')
	list_display = ('id','title','asked_by','created_date','question_owner')
	list_display_links = ('id','title','asked_by')
	search_fields = ('title',)
	list_filter = ('title',)
	ordering = ('id',)
	readonly_fields = ('created_date',)
	actions = None
	resource_class = QuestionResource
	inlines = [AnswerAdminInline]
	# can_delete = False

	def has_delete_permission(self, request, obj=None):
		return False

	#its working
	# def __init__(self, *args, **kwargs):
	# 	super(QuestionAdmin, self).__init__(*args, **kwargs)
	# 	self.list_display_links = (None, )

	# http://127.0.0.1:8000/admin/accounts/person/2/
	# http://127.0.0.1:8000/admin/stackapp/question/3/

	def question_owner(self,obj):
		import pdb; pdb.set_trace()    
		# url = reverse("admin:%s_change"%(obj.asked_by.id),args=[obj.asked_by.id])
		# reverse( 'django-admin', args=["%s/%s/%s/" % (app_label, model_name, obj_id)] )
		url = reverse("admin:%s_%s_change"%('accounts','person'),args=[obj.asked_by.id])
		# url = reverse("admin:%s_%s_change"%('user',''),args=[obj.asked_by.id])
		return "<a href=%s>%s</a>"%(url,obj.asked_by.id)    

  	question_owner.allow_tags = True


	def has_add_permission(self, request):
		return True

admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(Vote)
admin.site.register(Hashtags)






