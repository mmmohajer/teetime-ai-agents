from django.db.models import F
from django.conf import settings
from django.core.cache import cache
import os
import re
import json
import uuid
from google.cloud import texttospeech
from pgvector.django import CosineDistance

from core.models import UserModel
from core.tasks import remove_generated_voice_by_ai_task
from ai.utils.open_ai_manager import OpenAIManager
from ai.utils.google_ai_manager import GoogleAIManager
from customer_support.constants import (
    ALL_TEA_TIME_SUB_PLANS,
    LIST_OF_GREETING_MESSAGES,
    LIST_OF_HOLDOING_MESSAGES,
)
from customer_support.models import CustomerSupportKnowledgeBaseChunkModel
from customer_support.utils.connection_config import ConnectionConfigManager


class TeeTimeSupportAgent:
    """
    Loop-proof support agent for TeeTime GolfPass.

    Uses:
    - OpenAIManager for text completions.
    - GoogleAIManager for TTS audio generation.
    """

    _APP_TASK_RE = re.compile(r'\{[^{}]*"app_task"[^{}]*\}', re.DOTALL)

    def __init__(self, session_id):
        """
        Initializes the TeeTimeSupportAgent with AI and Google managers and a connection manager.

        Args:
            cur_users (list, optional): List of current users for context. Defaults to [].
        """
        cur_user = UserModel.objects.filter(email="mohammad@teetimegolfpass.com").first()
        self.open_ai_manager = OpenAIManager(model="gpt-4", api_key=settings.OPEN_AI_SECRET_KEY, cur_users=[cur_user])
        self.google_manager = GoogleAIManager(api_key=settings.GOOGLE_API_KEY, cur_users=[cur_user])
        self.connection_manager = ConnectionConfigManager()
        self.session_id = session_id
    # ----------------------
    # Knowledge base search
    # ----------------------
    def _find_similar_chunks(self, user_question, top_k=3, similarity_threshold=0.3):
        """
        Finds the most similar knowledge base chunks to the user's question using vector similarity.

        Args:
            user_question (str): The user's question to search for.
            top_k (int, optional): Number of top similar chunks to return. Defaults to 3.
            similarity_threshold (float, optional): Maximum similarity distance. Defaults to 0.3.

        Returns:
            str: Concatenated relevant content or a message if nothing is found.
        """
        try:
            user_chunk = self.open_ai_manager.build_materials_for_rag(text=user_question[:2000], max_chunk_size=2000)
            user_embedding = user_chunk.get("vector") or ""
            returned_str = ""
            search_results = (
                CustomerSupportKnowledgeBaseChunkModel.objects
                .annotate(similarity=CosineDistance(F("embedding"), user_embedding))
                .filter(similarity__lte=similarity_threshold)
                .order_by("similarity")[:top_k]
            )
            for chunk in search_results:
                returned_str += f"{chunk.kb.url}\nContent: {chunk.chunk_text}\n\n"

            return returned_str.strip() if returned_str else "No relevant information found."
        except Exception as e:
            print(f"Error finding similar chunks: {e}")
            return "No relevant information found."
    
    # ----------------------
    # Query backends
    # ----------------------
    def _safe_json(self, obj):
        """
        Safely serializes an object to a pretty-printed JSON string.

        Args:
            obj: Any serializable Python object.

        Returns:
            str: JSON string representation of the object.
        """
        def default(o):
            return str(o)
        return json.dumps(obj, ensure_ascii=False, indent=2, default=default)

    def _query_user(self, user_email):
        """
        Looks up user information in the production database and Zoho CRM by email.

        Args:
            user_email (str): The user's email address.

        Returns:
            str: JSON string with user info from DB and Zoho, or 'NO_ACCOUNT' if not found.
        """
        query = f"""
            SELECT * 
            FROM public."user" u
            JOIN public."user_product" up ON up.user_id = u.id
            JOIN product p ON up.product_id = p.id
            WHERE u.email = '{user_email}'
        """
        user_info_from_db = self.connection_manager.connect_to_prod_app_db(query)
        
        criteria = f"(Email_1:equals:{user_email})"
        user_info_from_zoho = self.connection_manager.send_zoho_crm_req(f"Sales_Orders/search?criteria={criteria}")

        info = {
            "from_db": user_info_from_db["data"] if user_info_from_db.get("success") else None,
            "from_zoho": user_info_from_zoho["data"] if user_info_from_zoho.get("success") else None,
        }

        if not info["from_db"] and not info["from_zoho"]:
            return "NO_ACCOUNT"

        return self._safe_json(info)


    def _query_general_data(self, question):
        """
        Finds and returns general knowledge base information relevant to the question.

        Args:
            question (str): The user's question.

        Returns:
            str or None: Relevant answer text, or None if not found.
        """
        raw = self._find_similar_chunks(question)
        text = raw if isinstance(raw, str) else self._safe_json(raw)
        if not text or not str(text).strip():
            return None
        low = text.lower()
        if "queryset []" in low or "no result" in low or "not found" in low:
            return None
        return text

    # ----------------------
    # Run logic
    # ----------------------
    def run_once(self):
        """
        Processes a single step of the conversation, handling tasks and generating responses.

        Returns:
            dict: The agent's response, including either a message or an app task.
        """
        out = self._model_decide()

        if "message_to_user" in out and not out.get("app_task"):
            self._append_assistant_json(out)
            return {"response": out}

        if "app_task" not in out:
            self._append_assistant_json(out)
            return {"response": out}

        self._append_assistant_json(out)
        app_task = out.get("app_task")

        if app_task == "query_general_data":
            question = (out.get("question") or "").strip()
            answer = self._query_general_data(question)

            if answer and str(answer).strip():
                payload = f"GENERAL_DATA_RESULT\nQuestion: {question}\nAnswer:\n{answer}"
            else:
                payload = f"GENERAL_DATA_RESULT\nQuestion: {question}\nNO_RESULT"

            self._append_to_history({"role": "company", "content": payload})
            final_out = self._model_decide()
            self._append_assistant_json(final_out)
            return {"response": final_out}

        if app_task == "query_user":
            email = (out.get("user_email") or "").strip()
            lookup_text = self._query_user(email)

            if lookup_text and str(lookup_text).strip() and lookup_text != "NO_ACCOUNT":
                company_payload = f"USER_LOOKUP_RESULT\n{lookup_text}"
            else:
                company_payload = "USER_LOOKUP_RESULT\nNO_ACCOUNT"

            self._append_to_history({"role": "company", "content": company_payload})
            final_out = self._model_decide()
            self._append_assistant_json(final_out)
            return {"response": final_out}

        self._append_to_history({"role": "company", "content": f"UNKNOWN_TASK\n{self._safe_json(out)}"})
        final_out = self._model_decide()
        self._append_assistant_json(final_out)
        return {"response": final_out}

    # ----------------------
    # Core model call
    # ----------------------
    def _model_decide(self, max_tokens=1000):
        """
        Builds the prompt, sends it to the AI model, parses and normalizes the response.

        Args:
            chat_history (list, optional): List of message dicts representing the conversation so far. If None, uses self._get_history().
            max_tokens (int, optional): Max tokens for the AI response. Defaults to 1000.

        Returns:
            dict: Parsed and normalized model output (app task or message).
        """
        chat_history = self._get_history()
        self.open_ai_manager.clear_messages()
        self.open_ai_manager.add_message("system", self._build_system_prompt())

        for chat in chat_history:
            role = self._map_role(chat.get("role", "user"))
            content = chat.get("content", "")
            if chat.get("role") == "company":
                content = f"[COMPANY_DATA]\n{content}"
                role = "assistant"
            self.open_ai_manager.add_message(role, text=content)
        raw = self.open_ai_manager.generate_response(max_token=max_tokens)
        try:
            obj = json.loads(raw)
        except Exception:
            embedded = self._extract_embedded_app_task(raw)
            obj = embedded if embedded else {"message_to_user": raw}

        obj = self._enforce_single_channel(obj)
        prev = self._last_assistant_app_task()

        if (
            obj.get("app_task")
            and prev
            and obj.get("app_task") == prev.get("app_task")
            and obj.get("question") == prev.get("question")
            and not self._has_company_since_last_app_task()
        ):
            return {
                "message_to_user": (
                    "Sorry—I couldn’t find relevant information for that just now. "
                    "Would you like me to try a different phrasing, or connect you with a human agent (Mon–Fri, 9am–5pm ET)?"
                )
            }

        if obj.get("app_task") == "query_general_data" and not obj.get("question"):
            last_user_msg = next((c.get("content", "") for c in reversed(chat_history) if c.get("role") == "user"), "")
            obj["question"] = last_user_msg or "No user question found."

        return obj

    def _build_system_prompt(self) -> str:
        """
        Builds the comprehensive system prompt for the AI agent with all instructions and knowledge.

        Returns:
            str: Complete system prompt including knowledge base, rules, and examples

        Usage Example:
            >>> agent = TeeTimeSupportAgent("session_123")
            >>> prompt = agent._build_system_prompt()
            >>> print(len(prompt))  # Shows the length of the comprehensive prompt
        """
        plans_json = json.dumps(ALL_TEA_TIME_SUB_PLANS, ensure_ascii=False, indent=2)

        return (
            "You are a phone call AI agent for TeeTime GolfPass. Respond based on the chat history.\n\n"
            "Here is the official knowledge base of all TeeTime subscription plans:\n"
            f"{plans_json}\n\n"
            "You must always prefer this knowledge base when answering questions about plans, pricing, coverage areas, renewal, or features.\n\n"

            "IMPORTANT: Never attempt to look up an account (query_user) until the user has provided an email address.\n"
            "When the user provides an email, always confirm it by repeating the email and spelling it out using the NATO alphabet, then ask 'Is this correct?' before sending the app_task.\n"
            "When confirming an email, only spell out the username part using the NATO alphabet. For well-known domains (like gmail.com, yahoo.com, outlook.com), say the domain and TLD normally (e.g., 'gmail dot com'), without spelling them out.\n\n"

            "---\n"
            "IMPORTANT: Always keep your answers as short and precise as possible. Share only the most essential information first.\n"
            "After giving a brief answer, make the call engaging by asking if the user would like to hear more or get extra details.\n"
            "For example: 'Would you like to hear more about this?' or 'Can I share additional details?'\n"
            "If the user is interested, you may then provide more information.\n"
            "---\n\n"

            "Example conversation:\n"
            "User: I need help with my account.\n"
            "Assistant: {\"message_to_user\":\"<speak>Sure, I can help with that. Could you please provide your email address so I can look up your account?</speak>\"}\n"
            "User: Yes, it's johndoe at gmail dot com.\n"
            "Assistant: {\"message_to_user\":\"<speak>Your email is johndoe@gmail.com. Spelled: j as juliet, o as oscar, h as hotel, n as november, d as delta, o as oscar, e as echo at g as golf, m as mike, a as alpha, i as india, l as lima dot c as charlie, o as oscar, m as mike. Is this correct?</speak>\"}\n"
            "User: Yes, that's correct.\n"
            "Assistant: {\"app_task\":\"query_user\",\"user_email\":\"johndoe@gmail.com\"}\n"
            "Company: [COMPANY_DATA]\\nUSER_LOOKUP_RESULT\\nNO_ACCOUNT\n"
            "Assistant: {\"message_to_user\":\"<speak>Sorry, I couldn't find any account associated with that email address. If you have another email, please provide it. Otherwise, I can connect you with a human agent.</speak>\"}\n"

            "Output contract (strict):\n"
            "- Your response must be a single valid JSON object.\n"
            "- Return exactly one of:\n"
            "  1) {\"message_to_user\":\"<speak>...</speak>\"} - ALL message_to_user content MUST be wrapped in SSML <speak> tags\n"
            "  2) An app task object.\n"
            "- Never include both keys. Never embed JSON inside strings. Never return an empty response.\n"
            "- MANDATORY: Every message_to_user MUST be valid SSML wrapped in <speak>...</speak> tags.\n\n"
            "App tasks:\n"
            "- query_user\n"
            "  Format: {\"app_task\":\"query_user\",\"user_email\":\"<email>\"}\n"
            "  Rules:\n"
            "  - Ask for the user's email first.\n"
            "  - Confirm the email by repeating it and spelling it with the NATO alphabet (including domain and TLD). "
            "Ask `Is this correct?` before sending the task.\n\n"
            "- query_general_data\n"
            "  Format: {\"app_task\":\"query_general_data\",\"question\":\"<concise question derived from the conversation>\"}\n"
            "  Rules:\n"
            "  - The question must be clear and specific based on the user's last request/context.\n"
            "  - When you trigger this task, return only the app task JSON.\n\n"
            "Company/backend messages are prefixed as:\n"
            "[COMPANY_DATA]\\n<content>\n\n"
            "Preferred normalized markers inside <content>:\n"
            "- GENERAL_DATA_RESULT\n"
            "  - Success: includes a line starting with \"Answer:\" followed by text → summarize to the user via message_to_user (do NOT trigger another task).\n"
            "  - No result: includes \"NO_RESULT\" → do NOT re-issue the same task. "
            "Respond with a short apology and ask to rephrase or offer human support.\n"
            "- USER_LOOKUP_RESULT\n"
            "  - Found account details → summarize next steps with message_to_user.\n"
            "  - No account (e.g., NO_ACCOUNT or wording like \"No account found\") → do NOT ask for the same app task again. "
            "Apologize, ask for an alternate email; if none, offer human support.\n\n"
            "Loop prevention:\n"
            "- Never repeat the same app task with the same parameters if there is no new [COMPANY_DATA] message since your last task.\n"
            "- After the backend answers an app task, respond with message_to_user, not another app_task, unless the user explicitly asks.\n\n"
            "Style & summarization:\n"
            "- Be concise, friendly, and helpful.\n"
            "- Use the official plan data above whenever possible.\n"
            "- When mentioning U.S. or Canadian states or regions, always expand abbreviations into their full names for clarity.\n"
            "  For example:\n"
            "    - NY → New York\n"
            "    - NJ → New Jersey\n"
            "    - PA → Pennsylvania\n"
            "    - VT → Vermont\n"
            "    - ME → Maine\n"
            "    - OH → Ohio\n"
            "    - MI → Michigan\n"
            "    - etc.\n"
            "- Never read state abbreviations letter by letter. Always prefer natural spoken names instead.\n"
            "- CRITICAL: Always return your message_to_user as valid SSML, wrapped in <speak>...</speak> tags.\n"
            "- Example SSML format: <speak>Hello! How can I help you today?</speak>\n\n"
            "Human support handoff:\n"
            "- If the user can't provide new info or asks for help, offer human support (Mon–Fri, 9am–5pm ET).\n"
        )

    
    def _append_to_history(self, new_message):
        """
        Appends a new message to the chat history in the cache for the current session.

        Args:
            new_message (dict): The message to append, e.g., {"role": ..., "content": ...}.

        Returns:
            list: The updated chat history after appending the new message.
        """
        key = f"chat_history_{self.session_id}"
        history = cache.get(key, [])
        history.append(new_message)
        cache.set(key, history, timeout=60*60)
        return history
    
    def _get_history(self):
        """
        Retrieves the chat history for the current session from the cache.

        Returns:
            list: The chat history as a list of message dicts, or an empty list if none exists.
        """
        return cache.get(f"chat_history_{self.session_id}", []) if self.session_id else []

    def _set_history(self, history):
        """
        Sets the chat history for the current session in the cache.

        Args:
            history (list): The chat history to store.
        """
        cache.set(f"chat_history_{self.session_id}", history, timeout=60 * 60 * 24)

    # ----------------------
    # Utilities
    # ----------------------
    def _extract_embedded_app_task(self, s):
        """
        Extracts a JSON object containing 'app_task' from a string, if present.

        Args:
            s (str): The string to search for an embedded app task.

        Returns:
            dict or None: The extracted app task dict, or None if not found or invalid.
        """
        if not isinstance(s, str):
            return None
        m = self._APP_TASK_RE.search(s)
        if not m:
            return None
        try:
            return json.loads(m.group(0))
        except Exception:
            return None

    def _enforce_single_channel(self, obj):
        """
        Ensures only one of 'app_task' or 'message_to_user' is present in the output.

        Args:
            obj (dict): The model's output object.

        Returns:
            dict: Normalized output with only one main key.
        """
        if not isinstance(obj, dict):
            return {"message_to_user": str(obj)}

        mtu = obj.get("message_to_user")
        if isinstance(mtu, str):
            embedded = self._extract_embedded_app_task(mtu)
            if embedded and "app_task" in embedded:
                clean = {k: v for k, v in embedded.items() if k != "app_task"}
                return {"app_task": embedded.get("app_task"), **clean}

        if "app_task" in obj:
            obj.pop("message_to_user", None)
            return obj
        if "message_to_user" in obj:
            obj.pop("app_task", None)
            return obj
        return {"message_to_user": json.dumps(obj, ensure_ascii=False)}

    def _last_assistant_app_task(self):
        """
        Finds the last assistant message in the chat history that included an app task.

        Args:
            chat_history (list, optional): List of message dicts. If None, uses self._get_history().

        Returns:
            dict or None: The last app task dict, or None if not found.
        """
        chat_history = self._get_history()
        for m in reversed(chat_history):
            if m.get("role") == "assistant":
                try:
                    j = json.loads(m.get("content", "{}"))
                    if isinstance(j, dict) and j.get("app_task"):
                        return j
                except Exception:
                    pass
        return None

    def _has_company_since_last_app_task(self):
        """
        Checks if there has been a company message since the last assistant app task.

        Args:
            chat_history (list, optional): List of message dicts. If None, uses self._get_history().

        Returns:
            bool: True if a company message was found after the last app task, else False.
        """
        
        chat_history = self._get_history()
        last_ai_idx = None
        for i in range(len(chat_history) - 1, -1, -1):
            m = chat_history[i]
            if m.get("role") == "assistant":
                try:
                    j = json.loads(m.get("content", "{}"))
                    if isinstance(j, dict) and j.get("app_task"):
                        last_ai_idx = i
                        break
                except Exception:
                    continue
        if last_ai_idx is None:
            return True
        for m in chat_history[last_ai_idx + 1:]:
            if m.get("role") == "company":
                return True
        return False

    def _append_assistant_json(self, obj):
        """
        Appends an assistant message (as JSON) to the chat history for the current session.

        Args:
            obj (dict): The assistant's response object to be serialized and appended.
        """
        self._append_to_history({"role": "assistant", "content": json.dumps(obj, ensure_ascii=False)})

    def _map_role(self, r):
        """
        Maps a role string to a valid role for the AI model.

        Args:
            r (str): The role string.

        Returns:
            str: A valid role ('system', 'user', 'assistant', or 'company').
        """
        return r if r in ("system", "user", "assistant", "company") else "user"

    # ----------------------
    # TTS and audio message generators
    # ----------------------
    def gpt_stt(self, text):
        """
        Converts text to speech using Google TTS and saves the audio file.

        Args:
            text (str): The text to convert to speech.

        Returns:
            str: The filename of the generated audio file.
        """
        audio_bytes = self.google_manager.tts(
            text=text,
            voice_name="en-US-Wavenet-F",
            audio_encoding=texttospeech.AudioEncoding.MP3,
        )
        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        with open(filepath, "wb") as f:
            f.write(audio_bytes)
        return filename

    def generate_holding_messages(self):
        """
        Generates and saves holding audio messages for each holding message in the list.

        Returns:
            None
        """
        for idx, message in enumerate(LIST_OF_HOLDOING_MESSAGES):
            audio_bytes = self.google_manager.tts(
                text=message,
                voice_name="en-US-Wavenet-F",
                audio_encoding=texttospeech.AudioEncoding.MP3,
            )
            path = os.path.join("/websocket_tmp/audio_messages/holding_messages", f"holding_{idx+1}.mp3")
            with open(path, "wb") as f:
                f.write(audio_bytes)
            print(f"Holding message {idx+1} saved to {path}")

    def generate_greeting_messages(self):
        """
        Generates and saves greeting audio messages for each greeting message in the list.

        Returns:
            None
        """
        for idx, message in enumerate(LIST_OF_GREETING_MESSAGES):
            audio_bytes = self.google_manager.tts(
                text=message,
                voice_name="en-US-Wavenet-F",
                audio_encoding=texttospeech.AudioEncoding.MP3,
            )
            path = os.path.join("/websocket_tmp/audio_messages/greeting_messages", f"greeting_{idx+1}.mp3")
            with open(path, "wb") as f:
                f.write(audio_bytes)
            print(f"Greeting message {idx+1} saved to {path}")

    def generate_bot_message(self, text):
        """
        Generates a bot audio message for the given text and schedules its removal.

        Args:
            text (str): The text to convert to speech.

        Returns:
            str: The URL to the generated bot audio message.
        """
        audio_bytes = self.google_manager.tts(
            text=text,
            voice_name="en-US-Wavenet-F",
            audio_encoding=texttospeech.AudioEncoding.MP3,
        )
        unique_name = f"bot_message_{uuid.uuid4().hex}.mp3"
        path = os.path.join("/websocket_tmp/audio_messages/bot_messages", unique_name)
        with open(path, "wb") as f:
            f.write(audio_bytes)
        remove_generated_voice_by_ai_task.apply_async((path,), countdown=600)
        return f"{settings.CLIENT_URL}/websocket_tmp/audio_messages/bot_messages/{unique_name}"

    def build_pre_defined_messages(self):
        self.generate_holding_messages()
        self.generate_greeting_messages()