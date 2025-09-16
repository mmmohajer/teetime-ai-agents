from celery import shared_task

from core.tasks.auth_tasks import send_activation_email_after_register, send_reset_password_email


@shared_task
def send_activation_email_after_register_task(user_id, redirect_url):
    send_activation_email_after_register(user_id, redirect_url)

@shared_task
def send_reset_password_email_task(user_id):
    send_reset_password_email(user_id)