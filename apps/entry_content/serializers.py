from rest_framework import serializers
from .models import Technology, ContentBlock

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

class ContentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentBlock
        fields = [
            'id',
            'type',
            'text_content',
            'file',
            'order',
            'created_at',
            'updated_at',
            'article',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        type = data.get('type')
        text_content = data.get('text_content')
        file = data.get('file')

        if type == ContentBlock.TEXT:
            if not text_content:
                raise serializers.ValidationError('Text content is required for text blocks.')
            if file:
                raise serializers.ValidationError('Text blocks must not have a file.')
        else:
            if not file:
                raise serializers.ValidationError('Multimedia blocks must have a file.')
            if text_content:
                raise serializers.ValidationError('Multimedia blocks must not have text content.')
        return data