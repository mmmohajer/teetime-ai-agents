from django.db import models

from core.models.base_model import TimeStampedModel
from core.models import UserModel


SERVICE_CHOICES = (
    ('OPEN_AI_COMPLETION', 'OPEN_AI_COMPLETION'),
    ('OPEN_AI_STT', 'OPEN_AI_STT'),
    ('OPEN_AI_EMBEDDING', 'OPEN_AI_EMBEDDING'),
    ('OPEN_AI_TTS', 'OPEN_AI_TTS'),
    ('OPEN_AI_IMAGE', 'OPEN_AI_IMAGE'),
    ('GOOGLE_COMPLETION', 'GOOGLE_COMPLETION'),
    ('GOOGLE_STT', 'GOOGLE_STT'),
    ('GOOGLE_EMBEDDING', 'GOOGLE_EMBEDDING'),
    ('GOOGLE_TTS', 'GOOGLE_TTS'),
    ('GOOGLE_IMAGE', 'GOOGLE_IMAGE'),
    ("GOOGLE_OCR", "GOOGLE_OCR"),
)

class AiCost(TimeStampedModel):
    user = models.ForeignKey(UserModel, blank=True, null=True, on_delete=models.SET_NULL, related_name="ai_costs")
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    service = models.CharField(max_length=255, choices=SERVICE_CHOICES)

    def __str__(self):
        return f"AI Cost for {self.user.email}: {self.cost}"

    class Meta:
        verbose_name_plural = "AI Costs"
        ordering = ('id',)

