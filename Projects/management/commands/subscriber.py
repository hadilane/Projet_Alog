""" from django.core.management.base import BaseCommand
import redis
import json
from django.conf import settings

class Command(BaseCommand):
    help = 'Subscribes to the Redis channel and processes events.'

    def handle(self, *args, **kwargs):
        r = redis.Redis.from_url(settings.CACHES['default']['LOCATION'])
        pubsub = r.pubsub()
        pubsub.subscribe('project_channel')
        self.stdout.write(self.style.SUCCESS('Subscribed to project_channel'))

        for message in pubsub.listen():
            if message and message['type'] == 'message':
                data = json.loads(message['data'])
                self.process_event(data)

    def process_event(self, data):
        event = data.get('event')
        if event == 'new_user':
            username = data.get('username')
            self.stdout.write(self.style.SUCCESS(f"New user registered: {username}"))
            # Process the event as needed, e.g., update database, send notifications, etc.
 """