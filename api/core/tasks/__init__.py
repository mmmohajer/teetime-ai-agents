from celery import shared_task

from core.tasks.auth_tasks import send_activation_email_after_register, send_reset_password_email
from core.tasks.helper import remove_generated_voice_by_ai


@shared_task
def send_activation_email_after_register_task(user_id, redirect_url):
    send_activation_email_after_register(user_id, redirect_url)

@shared_task
def send_reset_password_email_task(user_id):
    send_reset_password_email(user_id)

@shared_task
def remove_generated_voice_by_ai_task(audio_file_path):
    remove_generated_voice_by_ai(audio_file_path)