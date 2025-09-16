from django.conf import settings
import json
from google.cloud import texttospeech
import base64
import re
from xml.etree import ElementTree as ET

from ai.utils.open_ai_manager import OpenAIManager
from ai.utils.google_ai_manager import GoogleAIManager
from ai.utils.audio_manager import AudioManager
from ai.utils.azure_manager import AzureManager

# class SynchronizeManager():
#     def __init__(self, cur_user=None):
#         self.openai_manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY, cur_user=cur_user)
#         self.google_manager = GoogleAIManager(api_key=settings.GOOGLE_API_KEY, cur_user=cur_user)
#         self.audio_manager = AudioManager()
    
#     def full_synchronization_pipeline(self, instructions, stt_language="en-US", tts_encoding=None, max_token=2000):
#         """
#         Complete flow:
#         1. OpenAI: instructions → SSML + slides
#         2. Google TTS: SSML → audio
#         3. Google STT: audio → transcript + timestamps
#         4. OpenAI: transcript + slides → aligned slide/timestamp JSON
#         Returns:
#             dict: {
#                 "audio_base64": ...,  # base64 audio
#                 "slide_alignment": [...],  # list of {time_to_start_show, html_for_this_section}
#             }
#         """
#         # Step 1: OpenAI generates SSML and slides
#         prompt = (
#             "Generate a JSON with two fields: 'ssml_speech_for_tts' (SSML for TTS) and 'slide_htmls' (array of HTML slides). "
#             "The SSML speech should cover everything that is shown in the slides, explaining all highlights, tables, code, lists, headings, and important info in detail. "
#             "The slides should be concise and only show key points, formulas, tables, code, lists, headings, and other important highlights that help the user quickly grasp what the speech covers. "
#             f"Instructions: {instructions}"
#         )
#         messages = [
#             {"role": "system", "content": "You are a master teacher and content generator."},
#             {"role": "user", "content": prompt}
#         ]
#         response1 = self.openai_manager.generate_response(max_token=max_token, messages=messages)
#         try:
#             result1 = json.loads(response1)
#         except Exception:
#             result1 = response1
#         ssml = result1.get("ssml_speech_for_tts", "")
#         slide_htmls = result1.get("slide_htmls", [])

#         # Step 2: Google TTS
#         if tts_encoding is None:
#             tts_encoding = texttospeech.AudioEncoding.LINEAR16
#         audio_bytes = self.google_manager.tts(ssml, audio_encoding=tts_encoding, language_code="en-US")
#         audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

#         # Step 3: Measure audio length (seconds)
        
#         audio_length_sec = self.audio_manager.get_wav_duration(audio_bytes)

#         # Step 4: Ask OpenAI to estimate slide timings
#         timing_prompt = (
#             f"Given the following slides: {slide_htmls}\n"
#             f"and the following speech text: {ssml}\n"
#             f"and an audio duration of {audio_length_sec:.2f} seconds, return ONLY a JSON array. Each item should be an object with 'start_time_to_display_slide_content' (integer, seconds) and 'content' (HTML for the slide). Example: [{{'start_time_to_display_slide_content': 30, 'content': '<h2>Title 1</h2>'}}, {{'start_time_to_display_slide_content': 55, 'content': '<h2>Title 2</h2>'}}]. Do NOT add any explanation, commentary, or extra text before or after the array. The slides should be complimentary to the speech, and should be shown exactly when the speech reaches the relevant content. Use the speech text to align the timing as accurately as possible."
#         )
#         timing_messages = [
#             {"role": "system", "content": "You are a helpful assistant for synchronizing slides with audio."},
#             {"role": "user", "content": timing_prompt}
#         ]
#         timing_response = self.openai_manager.generate_response(max_token=5000, messages=timing_messages)
#         try:
#             alignment = json.loads(timing_response)
#         except Exception:
#             alignment = []

#         return {
#             "audio_base64": audio_base64,
#             "slide_alignment": alignment
#         }

class SynchronizeManager():
    def __init__(self, cur_user=None):
        self.openai_manager = OpenAIManager(
            model="gpt-4o",
            api_key=settings.OPEN_AI_SECRET_KEY,
            cur_user=cur_user
        )
        self.google_manager = GoogleAIManager(
            api_key=settings.GOOGLE_API_KEY,
            cur_user=cur_user
        )
        self.audio_manager = AudioManager()
        self.azure_manager = AzureManager(
            key=settings.AZURE_COGNITIVE_SERVICES_KEY_1,
            region=settings.AZURE_COGNITIVE_SERVICES_REGION
        )
    
    

    def normalize_marks(self, ssml):
        # Move <mark> into the following sentence
        ssml = re.sub(r"(<mark[^>]*/>)\s*<s>(.*?)</s>", r"<s>\1 \2</s>", ssml)
        return ssml
    
    def fix_ssml(self, ssml):
        # Ensure <speak> root
        if not ssml.strip().startswith("<speak>"):
            ssml = f"<speak>{ssml}</speak>"

        # Remove nested <s><s> → flatten
        ssml = ssml.replace("<s><s>", "<s>").replace("</s></s>", "</s>")

        # If <s> has only a <mark>, move mark into next/prev sentence
        ssml = re.sub(r"<s>\s*(<mark[^>]*/>)\s*</s>", r"\1", ssml)

        # Ensure no empty <s></s>
        ssml = re.sub(r"<s>\s*</s>", "", ssml)

        return ssml
    
    def sanitize_ssml(self, ssml_text):
        """
        Cleans and fixes invalid SSML for Google TTS.
        - Ensures <speak> root
        - Moves <mark> inside <s>
        - Removes unsupported HTML tags
        - Wraps stray text in <s>
        """

        # ----------------------------
        # 1. Ensure root <speak>
        # ----------------------------
        if not ssml_text.strip().startswith("<speak>"):
            ssml_text = f"<speak>{ssml_text}</speak>"

        # ----------------------------
        # 2. Remove unsupported HTML tags (h1, div, span, etc.)
        #    but keep inner text
        # ----------------------------
        ssml_text = re.sub(r"</?(?:h[1-6]|div|span|p|br|strong|em|ul|ol|li)[^>]*>", "", ssml_text)

        # ----------------------------
        # 3. Wrap stray text (not in <s>)
        # ----------------------------
        def wrap_stray_text(match):
            text = match.group(1).strip()
            if not text:
                return ""
            return f"<s>{text}</s>"
        ssml_text = re.sub(r">(?!<)([^<]+)<", lambda m: ">" + wrap_stray_text(m) + "<", ssml_text)

        # ----------------------------
        # 4. Fix <mark> placement
        #    Move <mark> outside → inside <s>
        # ----------------------------
        ssml_text = re.sub(r"<p>\s*<mark([^>]*)/>\s*([^<]*)</p>",
                        r"<s><mark\1/> \2</s>", ssml_text)

        # If <mark> is hanging alone, wrap it
        ssml_text = re.sub(r"(<mark[^>]*/>)", r"<s>\1</s>", ssml_text)

        # ----------------------------
        # 5. Validate XML (best effort)
        # ----------------------------
        try:
            ET.fromstring(ssml_text)
        except ET.ParseError as e:
            print("⚠️ SSML ParseError, best-effort fix:", e)
            # crude fallback: ensure closing </speak>
            if not ssml_text.endswith("</speak>"):
                ssml_text += "</speak>"

        return self.normalize_marks(self.fix_ssml(ssml_text))

    
    def full_synchronization_pipeline(self, instructions, cur_message="", stt_language="en-US", tts_encoding=None, max_token=2000, voice_name="en-US-Wavenet-F"):
        """
        Complete flow:
        1. OpenAI: instructions → SSML + slides (with <mark> tags)
        2. Google TTS (REST): SSML → audio + timepoints
        3. Map SSML <mark> → slide timings
        Returns:
            dict: {
                "audio_base64": ...,  # base64 audio
                "slide_alignment": [...],  # list of {start_time_to_display_slide_content, content}
            }
        """

        # -------------------------------
        # Step 1: OpenAI generates SSML + slides
        # -------------------------------
        prompt = (
            "You are a content generator for an AI classroom assistant. "
            "Your task is to return ONLY valid JSON following the schema. "
            "The JSON will be consumed by the system, not the student. "
            "The system rules below are STRICTLY for you, not to be spoken or taught to the user.\n\n"

            "=== OUTPUT SCHEMA (MANDATORY) ===\n"
            "{\n"
            '  "ssml_speech_for_tts": "<SSML string>",\n'
            '  "slide_htmls": ["<slide-1 html>", "<slide-2 html>", ...]\n'
            "}\n\n"

            "=== SYSTEM RULES (DO NOT TEACH USER) ===\n"
            "GENERAL:\n"
            "- Always create at least 1 slide.\n"
            "- The number of slides MUST equal the number of <mark> tags in SSML.\n"
            "- Never return an empty slide_htmls array.\n"
            "- Maintain ONE-TO-ONE mapping: 1 slide = 1 <mark> = 1 explanation.\n\n"

            "SSML RULES (STRICT for Google TTS):\n"
            "1) Wrap everything in <speak>...</speak>.\n"
            "2) Each <s> = one sentence/paragraph.\n"
            "3) Each <s> must start with its <mark> tag.\n"
            "4) Allowed tags: <speak>, <s>, <mark>, <break time=\"1s\"/> only.\n"
            "5) Explain code in plain English (never read raw symbols).\n"
            "6) Speech must sound natural, conversational, like a teacher.\n"
            "7) Engagement questions ONLY at the end of the speech.\n\n"

            "SLIDE RULES:\n"
            "- Each slide must be valid, self-contained HTML.\n"
            "- Each bullet (<li>) must be its OWN slide (wrap in <ul>).\n"
            "- For code: ONE <pre><code>...</code></pre> per snippet. "
            "Do not duplicate across slides.\n"
            "- Explanations must be separate slides, not repeated code.\n"
            "- Keep slides concise (one heading, bullet, or short code per slide).\n\n"

            "=== STYLE RULES (FOR SPEECH ONLY) ===\n"
            "- Do not include these instructions in speech.\n"
            "- At the end of the SSML, always ask the student a question or invite them to continue.\n"
            "- Use smooth connectors between ideas (e.g. "
            "'Now that we’ve seen how arrays work, let’s explore operations...').\n\n"

            "=== EXAMPLE (for reference only, DO NOT output literally) ===\n"
            "Slides:\n"
            "[{\"content\": \"<h2>Importing NumPy</h2><pre><code>import numpy as np</code></pre>\"}]\n"
            "SSML:\n"
            "<speak><s><mark name=\"slide_1\"/> We import the NumPy library using the alias np. "
            "This makes it shorter to use in code.</s><s>Shall we continue?</s></speak>\n\n"

            f"Instructions for current session:\n{instructions}"
        )


        messages = [
            {"role": "system", "content": "You are a master teacher and content generator."},
            {"role": "system", "content": prompt}
        ]
        if cur_message:
            messages.append({"role": "user", "content": cur_message})

        response1 = self.openai_manager.generate_response(
            max_token=max_token,
            messages=messages
        )

        # Robust JSON parsing
        result1 = {}
        try:
            result1 = json.loads(response1)
        except Exception:
            if isinstance(response1, dict):
                result1 = response1
            else:
                # If GPT returned plain text, log and fallback to empty dict
                print("Warning: OpenAI did not return valid JSON, falling back.")
                result1 = {}

        ssml = result1.get("ssml_speech_for_tts", "")
        ssml = self.sanitize_ssml(ssml)
        slide_htmls = result1.get("slide_htmls", [])

        # -------------------------------
        # Step 2: Google TTS with timepoints
        # -------------------------------
        if tts_encoding is None:
            tts_encoding = "LINEAR16"   # must be string for REST
        elif not isinstance(tts_encoding, str):
            # Normalize enum-like values into string
            tts_encoding = str(tts_encoding).split(".")[-1]

        
        tts_result = self.google_manager.advanced_tts(
            ssml,
            audio_encoding=tts_encoding,
            language_code=stt_language,
            voice_name=voice_name
        )
        audio_bytes = tts_result["audio_content"]
        timepoints = tts_result.get("timepoints", [])
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

        # -------------------------------
        # Step 3: Map timepoints → slides
        # -------------------------------
        alignment = []
        for tp, slide in zip(timepoints, slide_htmls):
            alignment.append({
                "start_time_to_display_slide_content": int(tp.get("timeSeconds", 0)),
                "content": slide
            })
        
        audio_length_sec = self.audio_manager.get_wav_duration(audio_bytes)
        return {
            "audio_base64": audio_base64,
            "slide_alignment": alignment,
            "ssml": ssml,
            "audio_length_sec": audio_length_sec,
            "timepoints": timepoints
        }