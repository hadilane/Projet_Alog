from django.db import models

from django.contrib.auth.models import AbstractUser
from api_users.models import *



# Category model
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProjectType(models.Model):
 type_name = models.CharField(max_length=100, unique=True)


# Project model
class Project(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    type = models.ForeignKey(ProjectType, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('completed', 'Completed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# ProjectImage model
class ProjectImage(models.Model):
    image = models.ImageField(upload_to='project_images/')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


   

# ProjectSkill model
class ProjectSkill(models.Model):
    user = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

# VolunteerApplication model
class VolunteerApplication(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)
    motivations = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Donation model
class Donation(models.Model):
    user = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donated_at = models.DateTimeField(auto_now_add=True)


