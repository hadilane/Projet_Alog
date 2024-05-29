from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import SimpleUserViewSet, SkillViewSet, UserSkillViewSet, OrganizationViewSet,AdminViewSet
router = DefaultRouter()
router.register(r'users', SimpleUserViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'user-skills', UserSkillViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'admin', AdminViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('trigger-simple-task/', views.trigger_simple_task, name='trigger_simple_task'),   
]
