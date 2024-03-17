from django.db import models
from shortuuid.django_fields import ShortUUIDField


class PrivateFile(models.Model):
    id = ShortUUIDField(primary_key=True)
    file = models.FileField(
        upload_to="private_files", default=None, blank=True, null=True
    )
    name = models.TextField(unique=True, default=None, blank=True, null=True)
    filetype = models.TextField(default=None, blank=True, null=True)
    notes = models.TextField(default=None, blank=True, null=True)
    metadata = models.JSONField(default=None, blank=True, null=True)


class LocalNotebook(models.Model):
    id = ShortUUIDField(primary_key=True)
    notebook = models.FileField(
        upload_to="local_notebooks", default=None, blank=True, null=True
    )
