from django.shortcuts import render
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