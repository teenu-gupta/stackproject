from django.contrib import admin

# Register your models here.

from  stackapp.models import Question, Answer , Vote , Hashtags

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Vote)
admin.site.register(Hashtags)

