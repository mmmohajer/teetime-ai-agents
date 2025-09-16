from django.db import models
import uuid
from storages.backends.s3boto3 import S3Boto3Storage


class TimeStampedModel(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class TimeStampedUUIDModel(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class MediaFileS3Storage(S3Boto3Storage):
    
    def __init__(self, is_public=False, bucket_name="", location="", *args, **kwargs):
        kwargs['location'] = location if location else ""
        kwargs['bucket_name'] = bucket_name if bucket_name else "media"
        kwargs['default_acl'] = "public-read" if is_public else "private"
        super().__init__(*args, **kwargs)