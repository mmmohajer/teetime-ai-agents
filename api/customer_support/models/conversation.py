from django.db import models
from django.conf import settings
from pgvector.django import VectorField

from core.models.base_model import TimeStampedModel


class CustomerSupportPhoneCall(TimeStampedModel):
    title = models.CharField(max_length=255, blank=True, null=True)
    conversation = models.JSONField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    call_sid = models.CharField(max_length=255, unique=True)
    already_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name_plural = "Customer Support Phone Calls"
        ordering = ('-updated_at',)