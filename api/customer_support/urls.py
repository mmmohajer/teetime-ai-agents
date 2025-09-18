from django.urls import path, include
from rest_framework import routers

from customer_support import views

urlpatterns = [
    path('knowledge-base/', views.KnowledgeBaseViewSet),
    path('customer-support/', views.CustomerSupportViewSet),
    path('twilio-voice/', views.TwilioVoiceWebhookViewSet),
]
