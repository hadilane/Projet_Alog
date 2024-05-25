# index_data.py

from django.core.management.base import BaseCommand
from elasticsearch.helpers import bulk
from .models import Project
from .document import ProjectDocument
from elasticsearch_dsl.connections import connections

class Command(BaseCommand):
    help = 'Index project data into Elasticsearch'

    def handle(self, *args, **options):
        # Delete existing index
        ProjectDocument._index.delete(ignore=404)

        # Create new index
        ProjectDocument.init()

        # Bulk indexing
        es = connections.get_connection()
        bulk(client=es, actions=(p.to_dict(True) for p in Project.objects.all().iterator()))
