from rest_framework import serializers

from customer_support.models import CustomerSupportKnowledgeBaseModel

class KnowledgeBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerSupportKnowledgeBaseModel
        fields = ['id', 'url', 'description',
                  'created_at', 'updated_at']        