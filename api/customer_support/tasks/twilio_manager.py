from django.core.cache import cache
from django.conf import settings
import json
import requests

from core.models import UserModel
from ai.utils.open_ai_manager import OpenAIManager
from customer_support.models import CustomerSupportConversationModel
from customer_support.utils.teetime_agent_manager import TeeTimeSupportAgent


def process_ai_response(call_sid, user_message):
    """
    Sends the user message to the backend AI, generates a bot response, and stores the result in cache.

    Args:
        call_sid (str): The unique call/session ID.
        user_message (str): The user's message to process.

    Returns:
        None
    """
    API_URL = f"{settings.CLIENT_URL}/api/customer-support/"
    payload = {
        "session_id": call_sid or "unknown",
        "user_message": user_message,
    }
    try:
        backend_response = requests.post(API_URL, json=payload, timeout=120).json() or {}
        bot_message = backend_response.get("bot_message") or ""
        agent = TeeTimeSupportAgent(call_sid)
        audio_url = agent.generate_bot_message(bot_message) if bot_message else None
        cache.set(f"{call_sid}_ai_response", {"text": bot_message, "audio_url": audio_url}, timeout=3600)
    except Exception as e:
        print(f"Error in processing AI response: {e}")
        cache.set(f"{call_sid}_ai_response", {"text": "Sorry, there was a problem processing your request.", "audio_url": None}, timeout=3600)

def chat_history_to_text(chat_history):
    """
    Converts a chat history list into a readable text transcript.

    Args:
        chat_history (list): List of message dicts with 'role' and 'content'.

    Returns:
        str: The conversation as a formatted string.
    """
    lines = []
    for msg in chat_history:
        content = msg["content"]
        if content.startswith("{") and "message_to_user" in content:
            try:
                content = json.loads(content).get("message_to_user", content)
            except Exception:
                pass
        lines.append(f'{msg["role"].capitalize()}: {content}')
    return "\n".join(lines)

def generate_summary_of_conversation(call_sid):
    """
    Summarizes the conversation history for a given call session using OpenAIManager.

    Args:
        call_sid (str): The unique call/session ID.

    Returns:
        dict: A dictionary with 'title' and 'summary' keys.
    """
    chat_history = cache.get(f"chat_history_{call_sid}", [])
    text_to_summarize = chat_history_to_text(chat_history)
    system_prompt = (
        "You are a customer support AI. Given the full conversation between a user and an assistant, "
        "summarize the key points and actions taken. "
        "Your summary should be clear, actionable, and help future users with similar issues. "
        "Make sure your summary includes all key points, such as any email address, phone number, or other personal information mentioned in the conversation. "
        "Return ONLY a JSON object in your response, in the format: {\"title\": <short_title>, \"summary\": <detailed_summary>}. Do not include any extra text."
    )
    cur_user = UserModel.objects.filter(email="mohammad@teetimegolfpass.com").first()
    openai_manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY, cur_users=[cur_user])
    openai_manager.clear_messages()
    openai_manager.add_message("system", system_prompt)
    openai_manager.add_message("user", text_to_summarize)
    raw_response = openai_manager.generate_response(max_token=2000)
    try:
        result = json.loads(raw_response)
        if not isinstance(result, dict):
            raise ValueError("Not a dict")
    except Exception:
        result = {
            "title": "Summary",
            "summary": raw_response.strip() or "No summary available."
        }

    return result

def save_chat_summary_to_db(call_sid):
    """
    Summarizes the conversation and saves the summary, title, and full chat history to a single CustomerSupportConversationModel instance.

    Args:
        call_sid (str): The unique call/session ID.

    Returns:
        obj: The CustomerSupportConversationModel instance.
    """
    """
    Summarizes the conversation and saves the summary, title, and full chat history to a single CustomerSupportPhoneCall instance.

    Args:
        call_sid (str): The unique call/session ID.

    Returns:
        obj: The CustomerSupportPhoneCall instance.
    """
    result = generate_summary_of_conversation(call_sid)
    title = result.get("title", "Summary")
    summary = result.get("summary", "")
    chat_history = cache.get(f"chat_history_{call_sid}", [])
    try:
        obj, _ = CustomerSupportConversationModel.objects.update_or_create(
            call_sid=call_sid,
            defaults={"title": title, "summary": summary, "conversation": chat_history}
        )
    except Exception as e:
        print(f"Error saving to CustomerSupportConversationModel: {e}")
        obj = None
    return obj