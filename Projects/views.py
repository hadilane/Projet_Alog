from django.shortcuts import render, get_object_or_404
from api_users.models import SimpleUser
from django.http import HttpResponse
from .models import Project
from django.core.cache import cache

def create_project(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')

        project = Project(title=title, description=description)
        project.save()

        return HttpResponse(f"Project created: {project.title}")
    return render(request, 'create_project.html')


def user_detail(request, username):
    user = get_object_or_404(SimpleUser, username=username)
    return render(request, 'home.html', {'user': user})

def display_cached_user(request, user_id):
    # Retrieve cached user data
    user = cache.get(f'user_{user_id}')
    if user:
        return HttpResponse(f"User {user.username} found in cache.")
    else:
        return HttpResponse("User not found in cache.")
    
def new_users(request):
    # Assuming you have a way to store and retrieve the new users list
    new_users_list = cache.get('new_users_list', [])
    return render(request, 'projects/new_users.html', {'new_users': new_users_list})