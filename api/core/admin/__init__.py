from django.conf import settings
from django.contrib import admin

from . import user, media, profile
from core.models import UserModel, MediaModel, ProfileModel

admin.site.site_header = "BASE REPO ADMIN DASHBOARD"

admin.site.register(UserModel, user.UserAdmin)
admin.site.register(MediaModel, media.MediaAdmin)
admin.site.register(ProfileModel, profile.ProfileAdmin)