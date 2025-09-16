from django.db import models
from django.conf import settings

from core.models.base_model import TimeStampedUUIDModel


class Profile(TimeStampedUUIDModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(blank=True, null=True, max_length=15)
    birth_date = models.DateField(null=True, blank=True)
    mailing_city = models.CharField(null=True, blank=True, max_length=255)
    mailing_province_state = models.CharField(null=True, blank=True, max_length=255)
    mailing_country = models.CharField(null=True, blank=True, max_length=255)
    mailing_street_address = models.CharField(null=True, blank=True, max_length=255)
    mailing_postal_code_zip = models.CharField(null=True, blank=True, max_length=20)
    profile_photo = models.CharField(null=True, blank=True, max_length=2048)
    credit = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = "Profiles"
        ordering = ('user__email',)
