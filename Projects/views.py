from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from .models import *
from api_users.models import *
from .serializers import *
from api_users.serializers import *
from django.http import JsonResponse
from elasticsearch_dsl import Search
from .document import ProjectDocument
from rest_framework.decorators import api_view
from elasticsearch import Elasticsearch
from django.utils.text import slugify
import re
from django.core.paginator import Paginator

ELASTIC_HOST = 'http://localhost:9200/'

# Create the client instance
client = Elasticsearch(
    [ELASTIC_HOST],
    basic_auth=('hadilane', '123456789')
)

# Viewsets for Category model
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Viewsets for Project model
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

# Viewsets for ProjectImage model
class ProjectImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer

# Viewsets for Projectskill model
class ProjectSkillViewSet(viewsets.ModelViewSet):
    queryset = ProjectSkill.objects.all()
    serializer_class = ProjectSkillSerializer

class ProjectTypeViewSet(viewsets.ModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer

# Viewsets for VolunteerApplication model
class VolunteerApplicationViewSet(viewsets.ModelViewSet):
    queryset = VolunteerApplication.objects.all()
    serializer_class = VolunteerApplicationSerializer

# Viewsets for Donation model
class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

# Template Views
def projects(request):
    projects = Project.objects.all()
    paginator = Paginator(projects, 5)  # Show 5 projects per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'projects': page_obj,  # Update this to use page_obj for pagination
    }
    
    return render(request, 'projects.html', context)

# Elasticsearch function
from elasticsearch_dsl import Q

# Elasticsearch function
@api_view(['POST'])
def search_projects(request, index='project_index'):
    query = request.data.get('query', '')
    category = request.data.get('category', '')  # Get category parameter from frontend
    project_type = request.data.get('type', '')  # Get type parameter from frontend

   # Split the query string into individual words
    query_words = query.split()
    search_fields = ['title^3']  # Fields to search
    # Preprocess each word of the query string
    processed_query_words = []
    for word in query_words:
        processed_word = re.sub(r'\W+', '', word)  # Remove special characters
        processed_word = slugify(processed_word)  # Convert spaces and special characters to hyphens
        processed_query_words.append(processed_word)

    queries = []
    # Construct the Elasticsearch query
    for processed_word in processed_query_words:
        fuzziness = 'AUTO'  # Set fuzziness to AUTO for approximate matching
        
        wildcard_query = "*" + query + "*"  # Adding wildcard characters to the query
        reversed_query = "*" + query[::-1] + "*"  # Adding wildcard characters to the reversed query

        # Define the Elasticsearch query using multi_match with wildcard pattern
        query = Q('bool', should=[
            Q('query_string', query=wildcard_query, fields=search_fields, fuzziness=fuzziness),
            Q('query_string', query=reversed_query, fields=search_fields, fuzziness=fuzziness)
        ], minimum_should_match=1)
        queries.append(query)

 

    # Combine queries with a boolean OR
    combined_query = Q('bool', should=queries)
    sort = '_score'  # Default sorting by relevance
    # Define the Elasticsearch query using Search
    search = Search(index=index).using(client).query(combined_query).sort(sort)

 # Sorting by category or type if provided
    
    if category and category != 'All':
      search = search.filter('match_phrase', category__name=category)

    if project_type:
      search = search.filter('match_phrase', type__type_name=project_type)

 
    # Execute the search
    results = search.execute()

    # Construct response data
    response_data = []
    for hit in results:
        # Extract image URLs from hit
        image_urls = [img['image_url'] for img in hit.image_url]

        response_data.append({
            'id': hit.meta.id,
            'title': hit.title,
            'description': hit.description,
            'category': hit.category.name if hasattr(hit, 'category') else None,
            'type': hit.type.type_name if hasattr(hit, 'type') else None,
            'image_urls': image_urls,
            'created_at': hit.created_at,
            'updated_at': hit.updated_at,
        })

    return Response(response_data)



def category_type_view(request):
    categories = CategoryViewSet.as_view({'get': 'list'})(request).data
    types = ProjectTypeViewSet.as_view({'get': 'list'})(request).data
    context = {'categories': categories, 'types': types}
    return render(request, 'your_template.html', context)