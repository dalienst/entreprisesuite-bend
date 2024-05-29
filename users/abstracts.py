import uuid

from django.db import models
from cloudinary.models import CloudinaryField


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UniversalIdModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        max_length=255,
    )

    class Meta:
        abstract = True


class AbstractProfileModel(models.Model):
    avatar = CloudinaryField("avatar", blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
