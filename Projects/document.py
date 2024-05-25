from elasticsearch_dsl import Document, Text, Keyword, Integer
from .models import *
from api_users.models import *
from django_elasticsearch_dsl import Document, fields

from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import Index, Text, Keyword, Date, Object

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

@registry.register_document
class ProjectDocument(Document):
   
    category = fields.ObjectField(
        properties={
            'name': fields.TextField(),
        }
    )

    type = fields.ObjectField(
        properties={
            'type_name': fields.TextField(),
        }
    )

    image_url = fields.ObjectField(
        properties={
            'image': fields.TextField(),
        }
    )

    # Add other fields as needed

    class Index:
        name = 'project_index'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
    class Django:
        model = Project
        fields = ['id', 'title', 'description', 'location', 'status', 'created_at', 'updated_at']
        related_models = [ProjectImage]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, ProjectImage):
            return related_instance.project.all()
    
    def prepare_image_url(self, instance):
        image_urls = []

        # Extract image URLs from ImageFieldFile objects
        for img in instance.projectimage_set.all():
            if img.image:
                image_urls.append({'image_url': img.image.url})
            else:
                image_urls.append({'image_url': ''})  # or any default value you want to set

        return image_urls