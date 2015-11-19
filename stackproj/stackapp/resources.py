from import_export import resources
from stackapp.models import Question , Answer , Vote , Hashtags

class QuestionResource(resources.ModelResource):
	class Meta:
		model = Question
		fields = ('id','title','asked_by','hashtag',)
		exclude = ('created_date',)
		export_order = ('id', 'title','hashtag' ,'asked_by',)
		import_id_fields = ('id',)


class AnswerResource(resources.ModelResource):
	class Meta:
		model = Answer
		fields = ('id','title')



class VoteResource(resources.ModelResource):
	class Meta:
		model = Vote

class HashtagsResource(resources.ModelResource):
	class Meta:
		model = Hashtags


