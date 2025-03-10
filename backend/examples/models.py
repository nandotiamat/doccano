import uuid

from django.contrib.auth.models import User
from django.db import models
from django_drf_filepond.models import DrfFilePondStoredStorage

from .managers import ExampleManager, ExampleStateManager
from projects.models import Project
from roles.models import Role

class Example(models.Model):
    objects = ExampleManager()

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    meta = models.JSONField(default=dict)
    filename = models.FileField(default=".", max_length=1024, storage=DrfFilePondStoredStorage())
    upload_name = models.CharField(max_length=512)
    annotations_approved_by_role = models.ForeignKey(to=Role, on_delete=models.SET_NULL, null=True, blank=True) 
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="examples")
    annotations_approved_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    score = models.FloatField(default=100)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def comment_count(self):
        return Comment.objects.filter(example=self.id).count()

    @property
    def data(self):
        if self.project.is_text_project:
            return self.text
        else:
            return str(self.filename)

    class Meta:
        ordering = ["created_at"]


class ExampleState(models.Model):
    objects = ExampleStateManager()
    example = models.ForeignKey(to=Example, on_delete=models.CASCADE, related_name="states")
    confirmed_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    confirmed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("example", "confirmed_by"),)


class Comment(models.Model):
    text = models.TextField()
    example = models.ForeignKey(to=Example, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def username(self):
        return self.user.username

    class Meta:
        ordering = ["created_at"]
