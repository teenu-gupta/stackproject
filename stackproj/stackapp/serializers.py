from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Question, Answer , Hashtags , Vote


class HashTagSerializers(serializers.ModelSerializer):
	class Meta:
		model = Hashtags
		fields = ('id','title','description')
		read_only_fields = ('id')


class AnswerSerializer(serializers.ModelSerializer):
	# answer = QuestionSerializer(many=True,read_only=True, required = False)
	class Meta:
		model = Answer
		fields = ('title','question','created_date','id')
		read_only_fields = ('id','answered_by',)	



class QuestionSerializer(serializers.ModelSerializer):
	# answer = AnswerSerializer(many=True,read_only=True, required = False)
	

	class Meta:
		model = Question
		
		fields = ('created_date','title','id','asked_by','hashtag')
		read_only_fields = ('id','asked_by',)




class QuestionAnswerSerializer(serializers.ModelSerializer):
	# answers = serializers.RelatedField(many=True,read_only=True,required = False)
	answer = AnswerSerializer(source='answer_of',many=True,read_only=True, required = False)
	# answer=serializers.StringRelatedField(many=True,read_only= True,required=False)
	
	class Meta:
		model = Question
		fields = ('created_date','id','answer','title','hashtag')
		# read_only_fields = ('answer')
		



class VoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vote
		fields = ('vote_type','voted_by','question','id','answer')
		read_only_fields = ('id','voted_by')











	
