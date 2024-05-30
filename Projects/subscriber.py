""" # app_project/subscriber.py

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

 """
 
import redis
import json
import django
import os
from django.conf import settings
from threading import Thread

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AlogProject.settings')
django.setup()

from api_users.models import SimpleUser

def handle_new_user(event_data):
    username = event_data['username']
    first_name = event_data['first_name']
    last_name = event_data['last_name']
    email = event_data['email']
    phone = event_data['phone']

    # Perform any actions needed with the user data
    print(f"New user registered: {username} ({first_name} {last_name}, {email}, {phone})")

def main():
    r = redis.Redis.from_url('redis://localhost:6360/0')
    p = r.pubsub()
    p.subscribe('project_channel')

    print("Subscribed to project_channel. Waiting for messages...")

    for message in p.listen():
        if message['type'] == 'message':
            event_data = json.loads(message['data'])
            if event_data.get('event') == 'new_user':
                handle_new_user(event_data)

if __name__ == '__main__':
    main()

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