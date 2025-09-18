from django.contrib import admin

class CustomerSupportPhoneCallAdmin(admin.ModelAdmin):
    list_display = ["title", "call_sid", "already_seen"]
    list_per_page = 10
    search_fields = ["title", "call_sid"]
    list_filter = ["already_seen"]

