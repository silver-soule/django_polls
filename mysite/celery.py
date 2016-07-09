from __future__ import absolute_import
from celery import Celery

app = Celery('mysite',
             broker='amqp://',
             include=['mysite.tasks'])
