import os

WITH_DOCKER = bool(int(os.environ.get("WITH_DOCKER", 0)))

if not WITH_DOCKER:
    from dotenv import load_dotenv
    load_dotenv()

from config.settings.constants import *
from config.settings.db import *
from config.settings.apps import *
from config.settings.middlewares import *
from config.settings.pass_validators import *
from config.settings.templates import *
from config.settings.celery import *
from config.settings.cache import *
from config.settings.email import *
from config.settings.rest_framework import *
from config.settings.channels import *

if not WITH_DOCKER:
    MIDDLEWARE.append('corsheaders.middleware.CorsMiddleware')
    CORS_ALLOWED_ORIGINS = ['http://localhost:3000']
    INSTALLED_APPS.append('corsheaders')