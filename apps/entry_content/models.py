from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import uuid

from django.conf import settings
from apps.accounts.models import CustomUser

# Create your models here.
class Technology(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='technologies')
    name = models.CharField(max_length=150)
    thumbnail = models.FileField(upload_to='content_files/technology', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Technologies"

        ordering = ['name']

    def __str__(self) -> str:
        return f"{self.name} - by {self.user_owner.username}"
    

class EntryContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Entry content types
    PROJECT = 'project'
    BLOG = 'blog'
    COMMENT = 'comment'
    ENTRY_CONTENT_TYPES = [
        (PROJECT, 'Project'),
        (BLOG, 'Blog'),
        (COMMENT, 'Comment'),
    ]

    # Entry content status
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    thumbnail = models.FileField(upload_to='content_files/entry_content', blank=True, null=True)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=ENTRY_CONTENT_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)

    technologies = models.ManyToManyField('Technology', related_name='entry_content', blank=True)
    parent_entry_content = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='comments'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title', '-created_at']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def clean(self):
        if self.type == self.COMMENT and not self.parent_entry_content:
            raise ValidationError('Comment entries must have a parent entry.')
        if self.type != self.COMMENT and self.parent_entry_content:
            raise ValidationError('Only comment entries can have a parent entry.')

    def __str__(self):
        return self.title
    

class ContentBlock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Content block type
    TEXT = 'text'
    IMAGE = 'image'
    VIDEO = 'video'
    GIF = 'gif'
    BLOCK_TYPES = [
        (TEXT, 'Text'),
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (GIF, 'GIF'),
    ]

    entry_content = models.ForeignKey(EntryContent, related_name='content_blocks', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=BLOCK_TYPES)

    # Content separation
    text_content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='content_files/content_block', blank=True, null=True)

    order = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def clean(self):
        if self.type == self.TEXT and not self.text_content:
            raise ValidationError('Text blocks must have text content.')
        if self.type != self.TEXT and not self.file:
            raise ValidationError('Multimedia blocks must have a file.')
        if self.type == self.TEXT and self.file:
            raise ValidationError('Text blocks must not have a file.')

    def __str__(self):
        return f'{self.type} - {self.entry_content.title}'