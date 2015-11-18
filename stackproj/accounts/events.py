from core.utils import Event
from django.contrib.auth import get_user_model
from accounts.models import Person
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

class UserRegistered(Event):
    code = 'user_registered'
    notify = 'email'
    app_name = 'accounts'

    def run(self, ctx):
        ctx['user'] = User.objects.get(id=ctx['user_id'])
        super(UserRegistered, self).run(ctx)

class UserEmailVerify(Event):
    code = 'email_verify'
    notify = 'email'
    app_name = 'accounts'

    def run(self, ctx):
        super(UserEmailVerify, self).run(ctx)


class UserResetPassword(Event):
    code = 'reset_password'
    notify = 'email'
    app_name = 'accounts'

    def run(self, ctx):
        super(UserResetPassword, self).run(ctx)

class UserEmailVerify(Event):
    code = 'email_verify'
    notify = 'email'
    app_name = 'accounts'

    def run(self, ctx):
        super(UserEmailVerify, self).run(ctx)
        
class UserChangePassword(Event):
    code = 'change_password'
    notify = 'email'
    app_name = 'accounts'
    
    def run(self, ctx):
        super(UserChangePassword, self).run(ctx)
        



