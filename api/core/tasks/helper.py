from django.core.cache import cache
from django.conf import settings
import os

def remove_generated_voice_by_ai(audio_file_path):
    if os.path.exists(audio_file_path):
        os.remove(audio_file_path)