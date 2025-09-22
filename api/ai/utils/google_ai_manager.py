from google.cloud import speech, texttospeech, vision
from google.generativeai import GenerativeModel, configure
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import tiktoken
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
import requests
import base64
import copy


from ai.utils.ai_manager import BaseAIManager
from ai.utils.audio_manager import AudioManager

class GoogleAIManager(BaseAIManager):
    def __init__(self, api_key=None, cur_users=[]):
        """
        Initialize the GoogleAIManager.

        Args:
            api_key (str): API key for Generative Language API (PaLM/Gemini).
            credentials_path (str): Path to Google service account JSON for other APIs.

        Returns:
            None
        """
        super().__init__(ai_type="google", cur_users=cur_users)
        if api_key:
            configure(api_key=api_key)
        self.speech_client = speech.SpeechClient()
        self.tts_client = texttospeech.TextToSpeechClient()
        self.vision_client = vision.ImageAnnotatorClient()
        self.model = GenerativeModel("models/gemini-1.5-pro-latest") if api_key else None
        self.GOOGLE_AI_PRICING = {
            "gemini-pro": {
                "input_per_1k_token": 0.0005,
                "output_per_1k_token": 0.0015,
            },
            "gemini-pro-vision": {
                "input_per_1k_token": 0.001,
                "output_per_1k_token": 0.003,
                "image_per_1_image": 0.002,
            },
            "speech-to-text": {
                "audio_stt_per_1_minute": 0.006,
            },
            "text-to-speech": {
                "tts_standard_per_1k_char": 0.016,
                "tts_premium_per_1k_char": 0.024,
            },
            "vision": {
                "image_per_1_image": 0.0015,
            },
        }

    def add_message(self, role, text=None, max_history=5):
        """
        Add a message to the conversation history. For Google Gemini, concatenates the last max_history turns in order,
        and summarizes earlier ones with an explanation at the beginning of the prompt.

        Args:
            role (str): One of 'system', 'user', 'assistant'.
            text (str): The text content.
            max_history (int): Maximum number of messages to keep in history. Default is 5.

        Returns:
            None

        Example:
            manager.add_message("user", text="Hello!")
        """
        if role not in ["system", "user", "assistant"]:
            return
        msg_text = text if text is not None else ""
        self.messages.append({"role": role, "content": msg_text})
        if len(self.messages) > max_history:
            old_msgs = self.messages[:-max_history]
            recent_msgs = self.messages[-max_history:]
            summary_lines = []
            system_lines = []
            for msg in old_msgs:
                if msg["role"] == "user":
                    summary_lines.append(f"User said: {msg['content']}")
                elif msg["role"] == "assistant":
                    summary_lines.append(f"Assistant said: {msg['content']}")
                elif msg["role"] == "system":
                    system_lines.append(f"System: {msg['content']}")
            summary_text = self.summarize("\n".join(summary_lines)) if summary_lines else ""
            system_text = "\n".join(system_lines)
            self.prompt = ""
            if summary_text:
                self.prompt += f"This is the summary of past conversations:\n{summary_text}\n"
            if system_text:
                self.prompt += f"System messages:\n{system_text}\n"
            self.prompt += f"\nNow, here are the last {max_history} messages in order:\n"
            for msg in recent_msgs:
                if msg["role"] == "user":
                    self.prompt += f"User: {msg['content']}\n"
                elif msg["role"] == "assistant":
                    self.prompt += f"Assistant: {msg['content']}\n"
                elif msg["role"] == "system":
                    self.prompt += f"System: {msg['content']}\n"
        else:
            self.prompt = ""
            for msg in self.messages:
                if msg["role"] == "user":
                    self.prompt += f"User: {msg['content']}\n"
                elif msg["role"] == "assistant":
                    self.prompt += f"Assistant: {msg['content']}\n"
                elif msg["role"] == "system":
                    self.prompt += f"System: {msg['content']}\n"
    
    def generate_response(self, max_token=2000, prompt=None):
        """
        Generate a response from the OpenAI chat model.
        
        Args:
            max_token (int): Maximum number of tokens in the response. Default is 2000.
            messages (list): List of message dicts. If None, uses internal history.
        
        Returns:
            str: The assistant's response text.
        
        Example:
            reply = manager.generate_response(max_token=500)
        """
        if not self.model:
            raise RuntimeError("Generative Language API not configured.")
        use_prompt = prompt if prompt is not None else getattr(self, "prompt", None)
        if not use_prompt:
            raise ValueError("Prompt is empty. Add messages before generating a response.")
        response = self.model.generate_content(use_prompt, generation_config={"max_output_tokens": max_token})
        enc = tiktoken.get_encoding("cl100k_base") 
        input_token_count = len(enc.encode(use_prompt))
        output_token_count = len(enc.encode(response.text))
        total_cost = (input_token_count / 1000) * self.GOOGLE_AI_PRICING["gemini-pro"]["input_per_1k_token"] + (output_token_count / 1000) * self.GOOGLE_AI_PRICING["gemini-pro"]["output_per_1k_token"]
        self._apply_cost(cost=total_cost, service="GOOGLE_COMPLETION")
        self.clear_messages()
        return response.text
    
    def stt(self, audio_bytes, language_code='en-US', encoding=None, file_path=None):
        """
        Perform speech-to-text using Google Cloud Speech-to-Text API.

        Args:
            audio_bytes (bytes): The input audio data.
            language_code (str): Language code of the audio. Default is 'en-US'.
            encoding: The audio encoding format (e.g., LINEAR16, MP3, FLAC).
            file_path (str): Optional path to the audio file (for duration calculation).

        Returns:
            dict: The transcription result.
        """
        if encoding is None:
            encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16

        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(content=audio_bytes)
        config = speech.RecognitionConfig(
            encoding=encoding,
            language_code=language_code,
            enable_automatic_punctuation=True
        )
        response = client.recognize(config=config, audio=audio)

        duration_seconds = None
        if hasattr(response, "total_billed_time") and response.total_billed_time:
            duration_seconds = response.total_billed_time.total_seconds()
        else:
            if encoding == speech.RecognitionConfig.AudioEncoding.LINEAR16:
                audio_manager = AudioManager()
                duration_seconds = audio_manager.get_wav_duration(audio_bytes)
            elif encoding == speech.RecognitionConfig.AudioEncoding.MP3 and file_path:
                try:
                    duration_seconds = MP3(file_path).info.length
                except Exception as e:
                    print(f"Error reading MP3 duration: {e}")
                    duration_seconds = 0
            elif encoding == speech.RecognitionConfig.AudioEncoding.FLAC and file_path:
                try:
                    duration_seconds = FLAC(file_path).info.length
                except Exception as e:
                    print(f"Error reading FLAC duration: {e}")
                    duration_seconds = 0

        duration_minutes = (duration_seconds / 60) if duration_seconds else 0
        price_per_minute = self.GOOGLE_AI_PRICING["speech-to-text"]["audio_stt_per_1_minute"]
        cost = duration_minutes * price_per_minute
        self._apply_cost(cost=cost, service="GOOGLE_STT")
        results = []
        for result in response.results:
            alt = result.alternatives[0]
            words = []
            for word_info in alt.words:
                words.append({
                    "word": word_info.word,
                    "start_time": word_info.start_time.total_seconds(),
                    "end_time": word_info.end_time.total_seconds()
                })
            results.append({
                "transcript": alt.transcript,
                "words": words
            })
        return results

    def tts(self, text, voice_name="en-US-Wavenet-D", audio_encoding=texttospeech.AudioEncoding.MP3, language_code="en-US", speaking_rate=1.0):
        """
        Perform text-to-speech using Google Cloud Text-to-Speech API.

        Args:
            text (str): The text to convert to speech.
            voice_name (str): The name of the voice to use. Default is "en-US-Wavenet-D".
            audio_encoding (str): The audio encoding format. Default is MP3.
            language_code (str): The language code for the voice. Default is "en-US".

        Returns:
            bytes: The audio content in the specified format.
        """
        client = texttospeech.TextToSpeechClient()
        if isinstance(text, str) and text.strip().startswith("<speak>"):
            input_text = texttospeech.SynthesisInput(ssml=text)
        else:
            input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            name=voice_name,
            language_code=language_code,
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=audio_encoding,
            speaking_rate=speaking_rate,
        )
        response = client.synthesize_speech(
            input=input_text,
            voice=voice,
            audio_config=audio_config,
        )

        char_count = len(text)
        if "Wavenet" in voice_name:
            price_per_1k = self.GOOGLE_AI_PRICING["text-to-speech"]["tts_premium_per_1k_char"]
        else:
            price_per_1k = self.GOOGLE_AI_PRICING["text-to-speech"]["tts_standard_per_1k_char"]
        cost = (char_count / 1000) * price_per_1k
        self._apply_cost(cost=cost, service="GOOGLE_TTS")
        return response.audio_content
    
    def advanced_tts(
        self,
        text,
        voice_name="en-US-Wavenet-D",
        audio_encoding="LINEAR16",     # keep LINEAR16 so your duration math works
        language_code="en-US",
        sample_rate_hz=16000,
        cred_path="/run/secrets/cred.json",
        speaking_rate=1.0
    ):
        """REST TTS with SSML <mark> timepoints (v1beta1)."""
        # --- Auth
        creds = service_account.Credentials.from_service_account_file(
            cred_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        creds.refresh(Request())
        token = creds.token
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        # --- SSML hygiene
        ssml = text if (isinstance(text, str) and text.strip().startswith("<speak>")) else f"<speak>{text}</speak>"

        # --- Base body (timepointing is TOP-LEVEL in REST)
        body = {
            "input": {"ssml": ssml},
            "voice": {"languageCode": language_code, "name": voice_name},
            "audioConfig": {"audioEncoding": audio_encoding, "sampleRateHertz": sample_rate_hz, "speakingRate": speaking_rate},
            "enableTimePointing": ["SSML_MARK"],
        }

        def _post(endpoint, payload, label):
            resp = requests.post(endpoint, headers=headers, json=payload)
            if not resp.ok:
                # log full body to see *why* it failed
                print(f"TTS error ({label}): {resp.status_code} {resp.text}")
                resp.raise_for_status()
            return resp.json()

        # 1) v1beta1 + requested voice + marks
        try:
            data = _post("https://texttospeech.googleapis.com/v1beta1/text:synthesize", body, "v1beta1+marks+voice")
        except requests.HTTPError:
            # 2) v1beta1 + STANDARD voice + marks
            try:
                b2 = copy.deepcopy(body)
                b2["voice"]["name"] = "en-US-Standard-C"
                data = _post("https://texttospeech.googleapis.com/v1beta1/text:synthesize", b2, "v1beta1+marks+standard")
            except requests.HTTPError:
                # 3) v1 without marks (last resort to still get audio)
                b3 = copy.deepcopy(body)
                b3.pop("enableTimePointing", None)
                data = _post("https://texttospeech.googleapis.com/v1/text:synthesize", b3, "v1+no-marks")

        audio_b64 = data.get("audioContent", "")
        timepoints = data.get("timepoints", [])
        return {
            "audio_content": base64.b64decode(audio_b64) if audio_b64 else b"",
            "timepoints": timepoints,
        }

    
    def generate_image_description(self, image_bytes):
        """
        Generate a description of an image using Google Cloud Vision API.

        Args:
            image_bytes (bytes): The input image data.

        Returns:
            str: The generated description of the image.
        """
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_bytes)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        descriptions = [label.description for label in labels]
        cost = self.GOOGLE_AI_PRICING["vision"]["image_per_1_image"]
        self._apply_cost(cost=cost, service="GOOGLE_IMAGE")
        return ", ".join(descriptions)