from rest_framework import serializers
from general.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username','full_name', 'date_of_birth', 'type', 'user']