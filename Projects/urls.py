from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'project', ProjectViewSet)
router.register(r'project_image', ProjectImageViewSet)
router.register(r'project_skill', ProjectSkillViewSet)
router.register(r'volunteer_application', VolunteerApplicationViewSet)
router.register(r'donation', DonationViewSet)
router.register(r'project_type', ProjectTypeViewSet)


urlpatterns = [
    path('home/', views.projects, name='projects'),
    path('search/', views.search_projects, name='search_projects'),
    path('projects/', include(router.urls)),
    path('user/<str:username>/', views.user_detail, name='user_detail'),
]
