from django.conf import settings
import boto3

class AwsManager:
    def __init__(self, access_key_id, secret_access_key, region_name):
        self.polly_client = boto3.client(
            "polly",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name
        )

    def list_voices(self, language_code="fa-IR"):
        """List available voices for a given language (e.g., fa-IR for Farsi)"""
        response = self.polly_client.describe_voices(LanguageCode=language_code)
        return [voice["Id"] for voice in response.get("Voices", [])]
    
    def tts(self, text, voice="Joanna", format="mp3", ssml=False):
        """
        Convert text (or SSML) to speech and return audio bytes.
        If ssml=True, treat input as SSML markup.
        """
        params = {
            "Text": text,
            "OutputFormat": format,
            "VoiceId": voice,
        }
        if ssml:
            params["TextType"] = "ssml"

        response = self.polly_client.synthesize_speech(**params)
        return response["AudioStream"].read()