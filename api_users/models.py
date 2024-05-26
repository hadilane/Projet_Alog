from django.db import models
from django.contrib.auth.models import AbstractUser

# User model
class SimpleUser(AbstractUser):
    role = models.CharField(max_length=10, choices=[('volunteer', 'Volunteer'), ('public', 'Public')], default='public')
    phone = models.CharField(max_length=10, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='simple_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='simple_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
        related_query_name='user',
    )
    def __str__(self):
        return self.username

# Skill model
class Skill(models.Model):
    skill = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# UserSkill model
class UserSkill(models.Model):
    user = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

# Organization model
class Organization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Admin model
class Admin(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)