from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Technology, ContentBlock, EntryContent
from django.contrib.auth import get_user_model

User = get_user_model()

class TechnologySerializer(serializers.ModelSerializer):
    user_owner = serializers.StringRelatedField()  # Read-only, displays the username

    class Meta:
        model = Technology
        fields = [
            'id',
            'name',
            'slug',
            'thumbnail',
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
            'entry_content',
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
    
class EntryContentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Change to editable PrimaryKeyRelatedField
    technologies = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Technology.objects.all()
    )

    class Meta:
        model = EntryContent
        fields = [
            'id',
            'title',
            'slug',
            'body',
            'author',
            'type',
            'status',
            'technologies',
            'parent_entry_content',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at'] 


class EntryContentDetailSerializer(EntryContentSerializer):
    content_blocks = ContentBlockSerializer(many=True, read_only=True)

    class Meta(EntryContentSerializer.Meta):
        fields = EntryContentSerializer.Meta.fields + ['content_blocks']