from django.apps import AppConfig


""" class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Projects'
 """

class ProjectConfig(AppConfig):
    name = 'Projects'

"""     def ready(self):
        from . import subscriber
        subscriber.start_listener() """