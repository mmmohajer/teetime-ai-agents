from django.urls import path, re_path

from . import consumers

URL_PATHS = [
    path("wss/test-socket/<room_id>/", consumers.TestSocketConsumer),
]
