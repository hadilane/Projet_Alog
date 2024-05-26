#projects/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_project, name='create_project'),
    path('new_users/', views.new_users, name='new_users'),
    path('user/<str:username>/', views.user_detail, name='user_detail'),

]
