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
    """

    _APP_TASK_RE = re.compile(r'\{[^{}]*"app_task"[^{}]*\}', re.DOTALL)

    def __init__(self, session_id):
        cur_user = UserModel.objects.filter(email="mohammad@teetimegolfpass.com").first()
        self.open_ai_manager = OpenAIManager(
            model="gpt-4",
            api_key=settings.OPEN_AI_SECRET_KEY,
            cur_users=[cur_user]
        )
        self.google_manager = GoogleAIManager(
            api_key=settings.GOOGLE_API_KEY,
            cur_users=[cur_user]
        )
        self.connection_manager = ConnectionConfigManager()
        self.session_id = session_id

    # ----------------------
    # Knowledge base search
    # ----------------------
    def _find_similar_chunks(self, user_question, top_k=3, similarity_threshold=0.3):
        try:
            user_chunk = self.open_ai_manager.build_materials_for_rag(
                text=user_question[:2000],
                max_chunk_size=2000
            )
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
        def default(o):
            return str(o)
        return json.dumps(obj, ensure_ascii=False, indent=2, default=default)

    def _query_user(self, user_email):
        query = f"""
            SELECT * 
            FROM public."user" u
            JOIN public."user_product" up ON up.user_id = u.id
            JOIN product p ON up.product_id = p.id
            WHERE u.email = '{user_email}'
        """
        user_info_from_db = self.connection_manager.connect_to_prod_app_db(query)

        criteria = f"(Email_1:equals:{user_email})"
        user_info_from_zoho = self.connection_manager.send_zoho_crm_req(
            f"Sales_Orders/search?criteria={criteria}"
        )

        info = {
            "from_db": user_info_from_db["data"] if user_info_from_db.get("success") else None,
            "from_zoho": user_info_from_zoho["data"] if user_info_from_zoho.get("success") else None,
        }

        if not info["from_db"] and not info["from_zoho"]:
            return "NO_ACCOUNT"

        return self._safe_json(info)

    def _query_general_data(self, question):
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

        self._append_to_history({
            "role": "company",
            "content": f"UNKNOWN_TASK\n{self._safe_json(out)}"
        })
        final_out = self._model_decide()
        self._append_assistant_json(final_out)
        return {"response": final_out}

    # ----------------------
    # Core model call
    # ----------------------
    def _model_decide(self, max_tokens=500):
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
            last_user_msg = next(
                (c.get("content", "") for c in reversed(chat_history) if c.get("role") == "user"),
                ""
            )
            obj["question"] = last_user_msg or "No user question found."

        return obj

    def _build_system_prompt(self) -> str:
        plans_json = json.dumps(ALL_TEA_TIME_SUB_PLANS, ensure_ascii=False, indent=2)
        return (
            "You are a phone call AI agent for TeeTime GolfPass. Respond based on the chat history.\n\n"
            f"Here is the official knowledge base of all TeeTime subscription plans:\n{plans_json}\n\n"
            "You must always prefer this knowledge base when answering questions..."
        )

    # ----------------------
    # History management
    # ----------------------
    def _append_to_history(self, new_message):
        key = f"chat_history_{self.session_id}"
        history = cache.get(key, [])
        history.append(new_message)
        cache.set(key, history, timeout=60 * 60)
        return history

    def _get_history(self):
        return cache.get(f"chat_history_{self.session_id}", []) if self.session_id else []

    def _set_history(self, history):
        cache.set(f"chat_history_{self.session_id}", history, timeout=60 * 60 * 24)

    # ----------------------
    # Utilities
    # ----------------------
    def _extract_embedded_app_task(self, s):
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
        chat_history = self._get_history()
        for m in reversed(chat_history):
            if m.get("role") == "assistant":
                content = m.get("content", {})
                if isinstance(content, str):
                    try:
                        content = json.loads(content)
                    except Exception:
                        continue
                if isinstance(content, dict) and content.get("app_task"):
                    return content
        return None

    def _has_company_since_last_app_task(self):
        chat_history = self._get_history()
        last_ai_idx = None
        for i in range(len(chat_history) - 1, -1, -1):
            m = chat_history[i]
            if m.get("role") == "assistant":
                content = m.get("content", {})
                if isinstance(content, str):
                    try:
                        content = json.loads(content)
                    except Exception:
                        continue
                if isinstance(content, dict) and content.get("app_task"):
                    last_ai_idx = i
                    break
        if last_ai_idx is None:
            return True
        for m in chat_history[last_ai_idx + 1:]:
            if m.get("role") == "company":
                return True
        return False

    def _append_assistant_json(self, obj):
        self._append_to_history({"role": "assistant", "content": obj})

    def _map_role(self, r):
        return r if r in ("system", "user", "assistant", "company") else "user"

    # ----------------------
    # TTS and audio generators
    # ----------------------
    def gpt_stt(self, text):
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
        for idx, message in enumerate(LIST_OF_HOLDOING_MESSAGES):
            audio_bytes = self.google_manager.tts(
                text=message,
                voice_name="en-US-Wavenet-F",
                audio_encoding=texttospeech.AudioEncoding.MP3,
            )
            path = os.path.join(
                "/websocket_tmp/audio_messages/holding_messages", f"holding_{idx+1}.mp3"
            )
            with open(path, "wb") as f:
                f.write(audio_bytes)

    def generate_greeting_messages(self):
        for idx, message in enumerate(LIST_OF_GREETING_MESSAGES):
            audio_bytes = self.google_manager.tts(
                text=message,
                voice_name="en-US-Wavenet-F",
                audio_encoding=texttospeech.AudioEncoding.MP3,
            )
            path = os.path.join(
                "/websocket_tmp/audio_messages/greeting_messages", f"greeting_{idx+1}.mp3"
            )
            with open(path, "wb") as f:
                f.write(audio_bytes)

    def generate_bot_message(self, text):
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
