# app_user/tasks.py

from celery import shared_task
import redis
from django.conf import settings
import json


@shared_task
def notify_project_service(data):
    try:
        print(f"Task data received: {data}")
        r = redis.Redis.from_url(settings.CACHES['default']['LOCATION'])
        if isinstance(data, dict):
            data = json.dumps(data)  # Ensure the data is serialized as JSON
        print(f"Data to publish: {data}")
        r.publish('project_channel', data)
    except Exception as e:
        print(f"An error occurred in the notify_project_service task: {e}")
        raise  # Re-raise the exception to be handled by Celery
    
@shared_task
def simple_task():
    print("Simple task executed successfully")