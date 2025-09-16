import os
from sendgrid import SendGridAPIClient

SG_SMTP = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY', ""))
USE_REAL_EMAIL_ADDRESSES = os.environ.get("USE_REAL_EMAIL_ADDRESSES", 0)
RECEIVER_EMAIL_FOR_TEST = os.environ.get(
    "RECEIVER_EMAIL_FOR_TEST", "RECEIVER_EMAIL_FOR_TEST")
EMAIL_ADDRESSES_FOR_TESTING = os.environ.get(
    'EMAIL_ADDRESSES_FOR_TESTING', '').split(',')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp4dev'
EMAIL_PORT = 25