from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets
from .models import *
from .serializers import *
from django.shortcuts import render
from django.http import HttpResponse
from .models import SimpleUser
from django.core.cache import cache
from .tasks import notify_project_service

# Viewsets for User model
class SimpleUserViewSet(viewsets.ModelViewSet):
    queryset = SimpleUser.objects.all()
    serializer_class = SimpleUserSerializer

# Viewsets for Skill model
class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class UserSkillViewSet(viewsets.ModelViewSet):
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer
    
# Viewsets for Organization model
class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

# Viewsets for Admin model
class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
#***********************************************************************************************************
#Template Views
def home(request):
    return render(request, 'home.html')



def register_user(request):
    if request.method == "POST":
        # Registration logic
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = SimpleUser(username=username, password=password, email=email)
        user.save()

        # Cache user count
        users_count = SimpleUser.objects.count()
        cache.set('users_count', users_count)

        # Notify other services
        notify_project_service.delay({"event": "new_user", "username": username})

        return HttpResponse(f"User registered. Total users: {users_count}")
    return render(request, 'register.html')
