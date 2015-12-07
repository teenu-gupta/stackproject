from core.utils import Event
from django.contrib.auth import get_user_model
from accounts.models import Person
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

class QuestionPosted(Event):
    code = 'question_posted'
    notify = 'email'
    app_name = 'stackapp'

    def run(self, ctx):
        ctx['user'] = User.objects.get(id=ctx['user_id'])
        super(QuestionPosted, self).run(ctx)