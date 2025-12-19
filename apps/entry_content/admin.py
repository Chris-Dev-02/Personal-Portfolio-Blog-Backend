from django.contrib import admin
from apps.entry_content.models import EntryContent, ContentBlock, Technology

# Register your models here.
@admin.register(EntryContent)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'type', 'created_at']

@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ['id', 'entry_content', 'type', 'order']

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_owner', 'description', 'created_at']