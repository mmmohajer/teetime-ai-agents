from customer_support.views import knowledge_base, phone_agent, twilio

KnowledgeBaseViewSet = knowledge_base.KnowledgeBaseViewSet.as_view()

CustomerSupportViewSet = phone_agent.CustomerSupportViewSet.as_view()

TwilioVoiceWebhookViewSet = twilio.TwilioVoiceWebhookViewSet.as_view()