from django.contrib import admin

from customer_support.models import CustomerSupportKnowledgeBaseModel, CustomerSupportKnowledgeBaseChunkModel

class CustomerSupportKnowledgeBaseModelAdmin(admin.ModelAdmin):
    list_display = ['url']
    list_per_page = 10
    search_fields = ['url']
    list_filter = ['url']


class CustomerSupportKnowledgeBaseChunkModelAdmin(admin.ModelAdmin):
    list_display = ['kb_url']
    list_per_page = 10
    search_fields = ['kb_url']
    list_filter = ['kb__url']

    def kb_url(self, obj):
        return obj.kb.url

class ZohoDeskTicketModelAdmin(admin.ModelAdmin):
    list_display = ['ticket_id']
    list_per_page = 10
    search_fields = ['ticket_id']