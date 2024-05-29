from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets
from .models import *
from .serializers import *
from django.core.cache import cache
from .tasks import notify_project_service,simple_task
import json
from django.http import HttpResponse
from .models import SimpleUser
from django.shortcuts import render
import requests
from AlogProject import settings

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
#***********************************************************************************************************

def register_user(request):
    if request.method == "POST":
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)

        result = r.json()
        if result['success']:
            # Registration logic
            username = request.POST.get('username')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            last_name = request.POST.get('last_name')
            user = SimpleUser(username=username, password=password, email=email,firstName=first_name,lastName=last_name,phone=phone)
            user.save()

            # Cache user count
            users_count = SimpleUser.objects.count()
            cache.set('users_count', users_count)

            # Notify other services
            event_data = {"event": "new_user", "username": username}
            notify_project_service.delay(event_data)  # Pass the data directly

            return HttpResponse(f"User registered. Total users: {users_count}")
        else:
            return HttpResponse("Invalid reCAPTCHA. Please try again.")
    return render(request, 'register.html', {'recaptcha_public_key': settings.RECAPTCHA_PUBLIC_KEY}
)

def trigger_simple_task(request):
    simple_task.delay()
    return HttpResponse("Simple task triggered")