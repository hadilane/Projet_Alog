from rest_framework import serializers
from .models import *
from api_users.models import *



# Serializer for Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = '__all__'

class ProjectSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSkill
        fields = '__all__'

class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = '__all__'

class VolunteerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerApplication
        fields = '__all__'

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ProjectImageSerializer(many=True)
    skills = ProjectSkillSerializer(many=True)
    class Meta:
        model = Project
        fields = '__all__'