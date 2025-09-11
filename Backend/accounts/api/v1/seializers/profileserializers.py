from rest_framework import serializers
from ....models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'gender', 'image', 'first_name', 'last_name', 'phone_number', 'birth_date', 'created_date', 'updated_date']