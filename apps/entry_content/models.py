from django.db import models
from django.contrib.auth.models import User
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