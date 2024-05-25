from django.shortcuts import render

from rest_framework import viewsets
from .models import *
from api_users.models import *
from .serializers import *
from api_users.serializers import *

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
    context = {'projects': projects}
    return render(request, 'projects.html', context)