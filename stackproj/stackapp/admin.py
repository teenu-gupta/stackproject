from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from  stackapp.models import Question, Answer , Vote , Hashtags
from stackapp.resources import QuestionResource

class QuestionAdmin(ImportExportModelAdmin):
	resource_class = QuestionResource
	pass


admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Vote)
admin.site.register(Hashtags)

