from django.db import models
from django.conf import settings
from pgvector.django import VectorField

from core.models.base_model import TimeStampedModel


class CustomerSupportKnowledgeBase(TimeStampedModel):
    url = models.TextField(max_length=2048, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name_plural = "Customer Support Knowledge Base Data"
        ordering = ('-updated_at',)

class CustomerSupportKnowledgeBaseChunk(TimeStampedModel):
    kb = models.ForeignKey(CustomerSupportKnowledgeBase, on_delete=models.CASCADE, related_name="chunks")
    chunk_text = models.TextField()
    embedding = VectorField(dimensions=3072)

    def __str__(self):
        return f"{self.kb.id}"

    class Meta:
        verbose_name_plural = "Customer Support Knowledge Base Chunks"
        ordering = ('-updated_at',)

class ZohoDeskTicket(TimeStampedModel):
    ticket_id = models.CharField(max_length=255, unique=True)
    details = models.JSONField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.ticket_id}"

    class Meta:
        verbose_name_plural = "Zoho Desk Tickets"
        ordering = ('-updated_at',)