from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from  stackapp.models import Question, Answer , Vote , Hashtags
from stackapp.resources import QuestionResource , AnswerResource
from datetime import datetime , timedelta
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from stackapp.events import QuestionPosted

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



def make_accepted(modeladmin, request, queryset):
	queryset.update(status='irrelevant')
make_accepted.short_description = "Mark selected questions as irrelevant"


class QuestionAdmin(ImportExportModelAdmin):

	# list_display = ('id','title','asked_by','created_date','question_owner')
	list_display = ('id','title','asked_by','created_date','question_owner','status')
	list_display_links = ('id','title','asked_by')
	search_fields = ('title',)
	list_filter = ('title',)
	ordering = ('id',)
	readonly_fields = ('created_date',)
	# actions = None
	resource_class = QuestionResource
	inlines = [AnswerAdminInline]
	actions = [make_accepted]
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
		# import pdb; pdb.set_trace()    
		# url = reverse("admin:%s_change"%(obj.asked_by.id),args=[obj.asked_by.id])
		# reverse( 'django-admin', args=["%s/%s/%s/" % (app_label, model_name, obj_id)] )
		url = reverse("admin:%s_%s_change"%('accounts','person'),args=[obj.asked_by.id])
		# url = reverse("admin:%s_%s_change"%('user',''),args=[obj.asked_by.id])
		return "<a href=%s>%s</a>"%(url,obj.asked_by.id)    

  	question_owner.allow_tags = True 


  	def save_model(self,request,obj,form,change):
  		# import pdb;pdb.set_trace()
		if change:
			question_status = Question.objects.get(id=obj.pk).status
			if obj.status == 'posted' and question_status == 'raised':
				q1 = QuestionPosted()


				q1.delay(ctx={'full_name':obj.asked_by.first_name,
					'question_title':obj.title,
					'question_id':obj.pk,
					'user_id': obj.asked_by.pk
					})

				obj.save()
			else:
				obj.save()


	def has_add_permission(self, request):
		return True

admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(Vote)
admin.site.register(Hashtags)






