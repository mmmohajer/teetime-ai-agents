from django.core.cache import cache
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework import views, permissions
from rest_framework.parsers import FormParser
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.request_validator import RequestValidator
import os
import random

from customer_support.utils.teetime_agent_manager import TeeTimeSupportAgent
from customer_support.tasks import process_ai_response_task, save_chat_summary_to_db_task
from customer_support.constants import LIST_OF_HOLDOING_MESSAGES, LIST_OF_GREETING_MESSAGES

API_URL = f"{settings.CLIENT_URL}/api/customer-support/"
VOICE_WEBHOOK_URL = f"{settings.CLIENT_URL}/api/twilio-voice/"

PREPARE_TWILIO_FOR_LISTENING = dict(
    input="speech",
    speech_timeout=str(2),
    action=VOICE_WEBHOOK_URL,
    method="POST",
    language="en-US",
    profanityFilter="true",
    bargeIn="false",
)

@method_decorator(csrf_exempt, name="dispatch")
class TwilioVoiceWebhookViewSet(views.APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [FormParser]

    def __init__(self, **kwargs):
        """
        Initializes the TwilioVoiceWebhookViewSet and its support agent.

        Args:
            **kwargs: Additional keyword arguments for the parent class.
        """
        super().__init__(**kwargs)
    
    def _twiml(self, r):
        """
        Converts a Twilio VoiceResponse object to an XML HttpResponse.

        Args:
            r: The Twilio VoiceResponse object.

        Returns:
            HttpResponse: XML response for Twilio.
        """
        return HttpResponse(str(r), content_type="text/xml")

    def _is_valid_twilio_request(self, request):
        """
        Validates the incoming request as a genuine Twilio webhook using the Twilio signature.

        Args:
            request: The Django request object.

        Returns:
            bool: True if the request is valid, False otherwise.
        """
        token = getattr(settings, "TWILIO_ACCOUNT_AUTH_TOKEN", None)
        if not token:
            return False
        validator = RequestValidator(token)
        signature = request.headers.get("X-Twilio-Signature", "")
        url = request.build_absolute_uri()
        params = request.POST.dict()
        return validator.validate(url, params, signature)

    def _make_twilio_ready_for_listening(self, vr, call_sid):
        """
        Prepares the Twilio VoiceResponse to listen for user input and redirects as needed.

        Args:
            vr: The Twilio VoiceResponse object.
            call_sid (str): The unique call/session ID.

        Returns:
            HttpResponse: XML response for Twilio to continue listening.
        """
        vr.pause(length=0.4)
        gather = Gather(**PREPARE_TWILIO_FOR_LISTENING)
        vr.append(gather)
        vr.redirect(VOICE_WEBHOOK_URL, method="POST")
        return self._twiml(vr)

    def post(self, request):
        """
        Handles incoming POST requests from Twilio, manages call flow, and responds with TwiML.

        Args:
            request: The Django request object.

        Returns:
            HttpResponse: XML response for Twilio.
        """
        if not self._is_valid_twilio_request(request):
            return HttpResponse("Invalid signature", status=403)

        call_sid = (request.POST.get("CallSid") or "").strip()
        teetime_agent = TeeTimeSupportAgent(session_id=call_sid)
        call_status = request.POST.get("CallStatus")
        user_message = (request.POST.get("SpeechResult") or "").strip()
        vr = VoiceResponse()

        if call_status == "completed":
            save_chat_summary_to_db_task.delay(call_sid)
            return HttpResponse("Call completed", status=200)

        chat_history = cache.get(f"chat_history_{call_sid}", [])
        is_first_interaction = not user_message and not chat_history

        if is_first_interaction or (user_message and user_message.strip() == "__CALL_STARTED__"):
            greeting_message = random.choice(LIST_OF_GREETING_MESSAGES)
            random_idx = random.randint(1, len(LIST_OF_GREETING_MESSAGES))
            google_greeting_path = f"/websocket_tmp/audio_messages/greeting_messages/greeting_{random_idx}.mp3"
            google_greeting_url = f"{settings.CLIENT_URL}{google_greeting_path}"
            teetime_agent._append_to_history({"role": "assistant", "content": greeting_message})
            if os.path.exists(google_greeting_path):
                vr.play(google_greeting_url)
            else:
                vr.say(greeting_message, voice="Polly.Joanna", language="en-US")
            return self._make_twilio_ready_for_listening(vr, call_sid)

        if user_message:
            cache.set(f"{call_sid}_user_message", user_message, timeout=3600)
            process_ai_response_task.delay(call_sid, user_message)
        ai_response = cache.get(f"{call_sid}_ai_response", None)
        if ai_response:
            audio_url = ai_response.get("audio_url") if isinstance(ai_response, dict) else None
            text = ai_response.get("text") if isinstance(ai_response, dict) else ai_response
            if audio_url:
                vr.play(audio_url)
            else:
                vr.say(text, voice="Polly.Joanna", language="en-US", ssml=True)
            cache.delete(f"{call_sid}_ai_response")
            return self._make_twilio_ready_for_listening(vr, call_sid)
        else:
            holding_message = random.choice(LIST_OF_HOLDOING_MESSAGES)
            random_idx = random.randint(1, len(LIST_OF_HOLDOING_MESSAGES))
            google_holding_path = f"/websocket_tmp/audio_messages/holding_messages/holding_{random_idx}.mp3"
            google_holding_url = f"{settings.CLIENT_URL}{google_holding_path}"
            if os.path.exists(google_holding_path):
                vr.play(google_holding_url)
            else:
                vr.say(holding_message, voice="Polly.Joanna", language="en-US")
            vr.pause(length=0.4)
            vr.redirect(VOICE_WEBHOOK_URL, method="POST")
            return self._twiml(vr)