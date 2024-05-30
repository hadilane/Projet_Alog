from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import requests
from rest_framework import viewsets
from .models import *
from .serializers import *
from django.shortcuts import render
from django.http import HttpResponse
from .models import SimpleUser
from django.core.cache import cache
from .tasks import notify_project_service,simple_task
import json

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
            user = SimpleUser(username=username, password=password, email=email, first_name=first_name,last_name=last_name,phone=phone)
            user.save()

            # Cache user count
            users_count = SimpleUser.objects.count()
            cache.set('users_count', users_count)
            # Cache the user object
            """  cache.set(f'user_{user.user_id}', user) """
            # Notify other services
            event_data = {
                "event": "new_user",
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone
            }
            notify_project_service.delay(event_data)

            return redirect('user_detail', username=username)
        else:
            return HttpResponse("Invalid reCAPTCHA. Please try again.")
    return render(request, 'register.html', {'recaptcha_public_key': settings.RECAPTCHA_PUBLIC_KEY}
)

def trigger_simple_task(request):
    simple_task.delay()
    return HttpResponse("Simple task triggered")