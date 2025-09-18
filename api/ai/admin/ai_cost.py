from django.contrib import admin

class AiCostAdmin(admin.ModelAdmin):
    list_display = ["user_email", "service", "cost"]
    list_per_page = 10
    search_fields = ["user__email", "service"]
    list_filter = ["service", "user__email"]

    def user_email(self, obj):
        return obj.user.email if obj.user else "N/A"

