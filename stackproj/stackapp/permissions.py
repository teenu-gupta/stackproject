from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from stackapp.models import Answer , Question
from rest_framework import exceptions, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, \
    IsAuthenticatedOrReadOnly
from rest_framework.views import APIView


class Permission_classes(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAuthenticatedOrReadOnly)


# class QuestionOwner(permissions.BasePermission):

# 	def has_permission(self,request):
# 		if Question.objects.filter(asked_by=request.user.id ):           
# 			return True
# 		return False
#         # except Question.DoesNotExist:
#         #     raise exceptions.PermissionDenied("Owner of question")

class QuestionOwnerValidation(permissions.BasePermission):
	
	def validate_questiondata(self,pk):

		# try:
			# ques_obj = get_object_or_404(Question, pk=pk, asked_by=self.request.user.id)

		ques_obj = Question.objects.filter(pk=pk, asked_by=self.request.user.id)
		if ques_obj:
			return Question.objects.get(pk=pk)
		else:
			raise PermissionDenied(detail="User can only update the questions posted by him")

		# except Question.DoesNotExist:
		# 	raise Http404

class AnswerOwnerValidation(permissions.BasePermission):
	def validate_answerdata(self,pk):
		# try:
		ans_obj = Answer.objects.filter(pk=pk,answered_by=self.request.user.id)
		if ans_obj:
			return Answer.objects.get(pk=pk)

		else:
			raise PermissionDenied(detail="User can only update the answers posted by him")
		# except Answer.DoesNotExist:
		# 	raise Http404



class QuestionNonOwner(permissions.BasePermission):

	def has_permission(self,request):
		ques_obj = Question.objects.get(id=request.data['question'],asked_by=request.user )
		if ques_obj:          
			return False
		else:
			return True
        # except Question.DoesNotExist:
        #     raise exceptions.PermissionDenied("Owner of question")


class QuestionNonOwnerValidation(object):


    # How to handle the True and False -- 404 was coming for the remaining conditions

    def validate_questiondata(self,request):
        # import ipdb;ipdb.set_trace()
    
        ques_obj = Question.objects.get(id= request.data['question'],
                                      asked_by=request.user) 


        if ques_obj:
            
            raise PermissionDenied(detail="User cannot vote on the question posted by him")
        else:
            return Question.objects.get(id=request.data['question'])

