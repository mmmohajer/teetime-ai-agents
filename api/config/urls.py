from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path(f'api/{settings.ADMIN_URL}/', admin.site.urls),
    path('api/', include('core.urls'))
]
