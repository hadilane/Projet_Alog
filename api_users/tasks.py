# app_user/tasks.py

from celery import shared_task
import redis
from django.conf import settings

@shared_task
def notify_project_service(data):
    try:
        r = redis.Redis.from_url(settings.CACHES['default']['LOCATION'])
        r.publish('project_channel', data)
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"An error occurred in the notify_project_service task: {e}")