from celery import shared_task

from customer_support.tasks.twilio_manager import process_ai_response
from customer_support.tasks.twilio_manager import process_ai_response, save_chat_summary_to_db

@shared_task
def process_ai_response_task(call_sid, user_message):
    process_ai_response(call_sid, user_message)

@shared_task
def save_chat_summary_to_db_task(call_sid):
    save_chat_summary_to_db(call_sid)