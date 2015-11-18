from django.shortcuts import render
from rest_framework import generics
from .models import Question , Answer , Vote , Hashtags
from .serializers import QuestionSerializer, AnswerSerializer , VoteSerializer , \
	QuestionAnswerSerializer , HashTagSerializers
from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from accounts.models import Person
from rest_framework.exceptions import PermissionDenied 
from accounts.serializers import PersonSerializer
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from stackapp.permissions import Permission_classes, QuestionOwnerValidation, AnswerOwnerValidation



# Create your views here.
class QuestionPost(generics.GenericAPIView):
	"""
	List all questions asked by an user 

	"""
	serializer_class = QuestionSerializer
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Question.objects.all()

	def get_serializer_class(self):
		return self.serializer_class

	def post(self,request):
		# import ipdb; ipdb.set_trace()

	
		serializer = self.serializer_class(data=request.data)


		if serializer.is_valid():
			serializer.validated_data['asked_by'] = request.user
			serializer.save()
			return Response(data=serializer.data,status= status.HTTP_200_OK)
		else:
			return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


class AnswerPost(generics.GenericAPIView):
	"""
	List all the answer asked for an question
	"""
	serializer_class = AnswerSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_serializer_class(self):
		return self.serializer_class

	def post(self,request):
		# import ipdb; ipdb.set_trace()

		serializer = self.serializer_class(data=request.data)

		quest_id = request.data['question']
		q = Question.objects.filter(id = quest_id , asked_by = request.user)

		
		if serializer.is_valid():
			if q:
				raise PermissionDenied(detail="You dont have permission to answer here") 
			else:
				serializer.validated_data['answered_by'] = request.user
				serializer.save()
				return Response(serializer.data,status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
		

class QuestionDetail(generics.GenericAPIView):
	"""
	Display all question asked by the user 

	"""	
	serializer_class = QuestionSerializer
	permission_classes = (permissions.IsAuthenticated,)
	model = Question
	
	def get_serializer_class(self):
		return self.serializer_class

	def get(self,request):
		# import ipdb;ipdb.set_trace()
		try:
			data = Question.objects.filter(asked_by=request.user.id)
		except Question.DoesNotExist:
		    data=None
		    print "Object Does Not Exist" 
		    raise Http404

		serializer = self.serializer_class(data,many=True)
		return Response(serializer.data,status=status.HTTP_200_OK)


class AnswerDetail(generics.GenericAPIView):
	"""
	Display all the answer list along with the details
	"""
	serializer_class = AnswerSerializer
	permission_classes = (permissions.IsAuthenticated,)
	model = Answer

	def get_serializer_class(self):
		return self.serializer_class

	def get(self,request):
		try:
			data= Answer.objects.filter(answered_by = request.user.id)
		except Answer.DoesNotExist:
			data = None
			print " Object Does Not Exist"
			raise Http404
		serializer =self.serializer_class(data,many=True)
		return Response(serializer.data,status= status.HTTP_200_OK)


class QuestionUpdate(Permission_classes,generics.GenericAPIView,QuestionOwnerValidation):

	"""
	Update and Delete the question

	"""
	serializer_class = QuestionSerializer
	# permission_classes = (permissions.IsAuthenticated,QuestionOwnerValidation,)
	model= Question



	def get(self,request,pk):
		# import ipdb;ipdb.set_trace()
		question_valid= self.validate_questiondata(pk)
		if question_valid:
			serializer=QuestionSerializer(question_valid)
			return Response(serializer.data,status=status.HTTP_200_OK)
		else:
			raise PermissionDenied(detail="You dont have permission to answer here")

	def delete(self,request,pk):
		question_valid= self.validate_questiondata(pk)
		if question_valid:
			try:
				obj= get_object_or_404(Question,id=pk)
				obj.delete()
				data = {"Details": "Question is deleted successfully"}
				return Response(data)
			except Question.DoesNotExist:
				raise Http404

	def put(self,request,pk):
		# import ipdb;ipdb.set_trace()
		question_valid= self.validate_questiondata(pk)
		if question_valid:
			obj = Question.objects.get(id=pk)
			obj.title = request.data['title']
			obj.asked = request.user.id

			serializer= self.serializer_class(obj,data=request.data)
			if serializer.is_valid():
				
				serializer.save()
				return Response(serializer.data,status=status.HTTP_200_OK)
			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class AnswerUpdate(Permission_classes,generics.GenericAPIView,AnswerOwnerValidation):
	"""
	Update and Delete the answer
	"""
	serializer_class = AnswerSerializer
	# permission_classes = (permissions.IsAuthenticated,)
	

	def get(self,request,pk):
		answer_valid = self.validate_answerdata(pk)
		if answer_valid:
			# answer = Answer.objects.get(id=pk)
			serializer=AnswerSerializer(answer_valid)
			return Response(data=serializer.data,status=status.HTTP_200_OK)
			

	def delete(self,request,pk):
		answer_valid = self.validate_answerdata(pk)
		if answer_valid:
			try:
				obj = Answer.objects.get(id=pk)
				obj.delete()
				# answer_valid.delete():
				data={"Details":"Answer deleted successfully"}
				return Response(data)
			except Answer.DoesNotExist:
				raise Http404

	def put(self,request,pk):
		# import ipdb; ipdb.set_trace()
		answer_valid= self.validate_answerdata(pk)
		if answer_valid:
			obj = Answer.objects.get(id=pk)
			
			serializer = self.serializer_class(obj,data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data,status=status.HTTP_200_OK)
			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class QuestionAnswerList(Permission_classes,generics.GenericAPIView,QuestionOwnerValidation):
	"""
	fetch the Question details along with the answer
	"""
	serializer_class = QuestionAnswerSerializer
	permission_classes = (permissions.IsAuthenticated,)
	model = Question
	

	def get(self,request,pk):
		import ipdb;ipdb.set_trace()

		data = self.model.objects.get(id=self.kwargs['pk'])
		
		
		serializer = self.serializer_class(data)

		return Response(serializer.data)

	
	# def get_queryset(self,kwargs):
	# 	return Question.objects.get(id=self.kwargs['pk'])

	# def get(self,request,pk):
	# 	serializer = self.serializer_class(data=request.data)
	# 	return Response(serializer.data,status=status.HTTP_200_OK)
	
	# def get(self,request,pk):
	# 	import ipdb;ipdb.set_trace()
	# 	# question_valid = self.validate_questiondata(pk)
	# 	# if question_valid:
	# 		# question = Question.objects.get(id=pk)
	# 		# data = []
	# 		# data.append(question)
	# 	try:
	# 		data = []

	# 		a  = Question.objects.get(id=pk)
	# 		if a:
	# 			data.append(a)
	# 		else:
	# 			data = []
	# 		answer = Answer.objects.filter(question=pk)
	# 		data.append(answer)

			
	# 		# serializer= self.serializer_class(data)	
	# 		# if serializer.is_valid():
	# 		serializer =self.serializer_class(data)
	# 		return Response(data=serializer.data,status=status.HTTP_200_OK)
	
	# 	except Answer.DoesNotExist:
	# 		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
		


class UserDashboard(generics.GenericAPIView):

	"""
	Get the question and answer count
	"""
	
	serializer_class = AnswerSerializer
	serializer_class = QuestionSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get(self,request):
		answer, question = 0,0
		answer = Answer.objects.filter(answered_by=request.user).count()
		question = Question.objects.filter(asked_by= request.user).count()
		return Response({'answer': answer,'question':question}, status = status.HTTP_200_OK)


class VotingQuestionAnswer(Permission_classes,generics.GenericAPIView):
	"""
	User is voting the question posted by other users
	"""
	serializer_class = VoteSerializer

	# permission_classes = (permissions.IsAuthenticated,QuestionNonOwner,)
	
	def post(self,request):
		import ipdb;ipdb.set_trace()


		if request.data['answer'] == 0 :
			ques_obj = Question.objects.get(id=request.data['question'])
			ques_list = Question.objects.filter(asked_by=request.user)

			vote_ques = Vote.objects.filter(question=request.data['question'],voted_by=request.user).count()
			try:
				if ques_obj in ques_list:
					raise PermissionDenied(detail="User cannot vote on the question posted by him")
				elif vote_ques > 0 :
					raise PermissionDenied(detail="User has already voted")
				else:

					serializer = self.serializer_class(data=request.data)
		
					if serializer.is_valid():
				
						serializer.validated_data['voted_by'] = request.user
				
						serializer.save()
						return Response(serializer.data,status=status.HTTP_200_OK)
			except Question.DoesNotExist:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
		elif request.data['question'] == 0 :
			ans_obj = Answer.objects.get(id=request.data['answer'])
			ans_list = Answer.objects.filter(answered_by=request.user)

			vote_ans = VoteAnswer.objects.filter(answer=request.data['answer'],voted_by=request.user).count()

			
			try:
				if ans_obj in ans_list:
					raise PermissionDenied(detail="User cannot vote on the answer posted by him")
				elif vote_ans > 0 :
					raise PermissionDenied(detail="User has already voted")
				else:

					serializer = self.serializer_class(data=request.data)
		
					if serializer.is_valid():
				
						serializer.validated_data['voted_by'] = request.user
				
						serializer.save()
						return Response(serializer.data,status=status.HTTP_200_OK)
			except Question.DoesNotExist:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class VotesQuesAnswerList(generics.ListAPIView):
	"""
	Display all the details of the Votes for an user
	"""
	model = Vote
	serializer_class = VoteSerializer
	queryset = Vote.objects.all()

	

class HashTagCreation(generics.GenericAPIView):
	"""
	Post hashtags for the question
	"""
	serializer_class = HashTagSerializers

	def post(self,request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class HashTagDetails(generics.ListAPIView):
	"""
	Fetch the hastag list
	"""
	serializer_class = HashTagSerializers
	serializer_class1 = QuestionSerializer
	queryset = Hashtags.objects.all()
	
