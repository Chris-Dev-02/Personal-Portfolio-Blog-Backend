from rest_framework import serializers
from .models import Technology

class TechnologySerializer(serializers.ModelSerializer):
    user_owner = serializers.StringRelatedField()  # Read-only, displays the username

    class Meta:
        model = Technology
        fields = [
            'id',
            'name',
            'image',
            'description',
            'created_at',
            'user_owner'
        ]