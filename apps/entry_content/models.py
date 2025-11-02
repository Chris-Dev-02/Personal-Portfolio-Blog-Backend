from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import uuid

# Create your models here.
class Technology(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='technologies')
    name = models.CharField(max_length=150)
    thumbnail = models.FileField(upload_to='content_files/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True)

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
    ARTICLE_TYPES = [
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
    thumbnail = models.FileField(upload_to='content_files/', blank=True, null=True)
    body = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=ARTICLE_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)

    technologies = models.ManyToManyField('Technology', related_name='entry-content', blank=True)
    parent_article = models.ForeignKey(
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
        if self.type == self.COMMENT and not self.parent_article:
            raise ValidationError('Comment entries must have a parent entry.')
        if self.type != self.COMMENT and self.parent_article:
            raise ValidationError('Only comment entries can have a parent entry.')

    def __str__(self):
        return self.title