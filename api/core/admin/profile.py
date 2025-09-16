from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['user_email', 'user_first_name',
                    'user_last_name', 'mailing_street_address']
    list_editable = ['mailing_street_address']
    list_per_page = 10
    list_select_related = ['user']
    search_fields = ['user__email__istartswith']

    @admin.display(ordering='user__email')
    def user_email(self, profile):
        return profile.user.email

    @admin.display(ordering='user__first_name')
    def user_first_name(self, profile):
        return profile.user.first_name

    @admin.display(ordering='user__last_name')
    def user_last_name(self, profile):
        return profile.user.last_name
