# app_project/subscriber.py

import redis
from django.conf import settings
from threading import Thread

def listen_to_user_service():
    r = redis.Redis.from_url(settings.CACHES['default']['LOCATION'])
    pubsub = r.pubsub()
    pubsub.subscribe('project_channel')

    for message in pubsub.listen():
        if message['type'] == 'message':
            handle_message(message['data'])

def handle_message(data):
    # Logic to handle messages from other services
    print(f"Received message: {data}")

def start_listener():
    listener_thread = Thread(target=listen_to_user_service)
    listener_thread.start()