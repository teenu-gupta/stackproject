from django.conf import settings
from celery import Task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.context import Context
from django.template.loader import get_template
# from push_notifications.models import APNSDevice, GCMDevice
# from requests.auth import HTTPBasicAuth
import logging
# import requests

logger = logging.getLogger('celery.task')


class Event(Task):
    notify = 'email', 'sms', 'mob','customer_care'
    code = 'event'

    email_templates = {'sub': 'core/emails/%s/%s_subject.txt',
                 'body': 'core/emails/%s/%s_body.txt',
                 'html': 'core/emails/%s/%s_body_html.txt'}

    # sms_template = 'core/sms/%s.txt'
    # mob_template = 'core/mob/%s/%s.txt'
    

    def __call__(self, *args, **kwargs):
        logger.info("starting to run")
        return self.run(*args, **kwargs)

    def do_actions(self, ctx):
        logger.info("running custom actions")
        actions = sorted(action for action in self.__class__.__dict__
                         if action.startswith('action'))
        for action in actions:
            getattr(self, action)(ctx)

    def send_emails(self, ctx):
        logger.info("sending email to user : %s", ctx['user'].email)
        subject = get_template(self.email_templates['sub'] % (self.app_name, self.code)
                               ).render(Context(ctx))
        subject = subject.replace('\n', ' ')
        body = get_template(self.email_templates['body'] % (self.app_name, self.code)
                            ).render(Context(ctx))
        html = get_template(self.email_templates['html'] % (self.app_name, self.code)
                            ).render(Context(ctx))
        sender = settings.COMM_EMAIL_SENDER
        recipient = ctx['user'].email
        email = EmailMultiAlternatives(subject,
                                       body,
                                       from_email=sender,
                                       to=[recipient])
        email.attach_alternative(html, "text/html")
        email.send()

    def send_emails_customer_care(self, ctx):

        logger.info("sending emails to customercare")
        subject = get_template(self.email_templates['sub'] % (self.app_name, self.code)
                               ).render(Context(ctx))
        subject = subject.replace('\n', ' ')
        body = get_template(self.email_templates['body'] % (self.app_name, self.code)
                            ).render(Context(ctx))
        html = get_template(self.email_templates['html'] % (self.app_name, self.code)
                            ).render(Context(ctx))
        sender = settings.COMM_EMAIL_SENDER
        if ctx['customer'] == 'True':
            recipient = ctx['email_id']
        else:    
            recipient = settings.TRADESGUY_CUSTOMER_CARE_TO_EMAIL
        email = EmailMultiAlternatives(subject,
                                       body,
                                       from_email=sender,
                                       to=[recipient])
        email.attach_alternative(html, "text/html")
        email.send()

    def send_notifications(self, ctx):
        if 'email' in self.notify:
            self.send_emails(ctx)
      

    def run(self, ctx):
        self.do_actions(ctx)
        self.send_notifications(ctx)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        logger.info("Ending run")
