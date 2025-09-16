from django.contrib import admin


class MediaAdmin(admin.ModelAdmin):
    list_display = ['title', 'file_type']
    list_per_page = 10
    search_fields = ['title__istartswith']