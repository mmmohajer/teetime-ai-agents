import azure.cognitiveservices.speech as speechsdk

class AzureManager:
    def __init__(self, key, region):
        self.speech_config = speechsdk.SpeechConfig(subscription=key, region=region)

    def list_voices(self, locale_prefix="fa-"):
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)
        voices = synthesizer.get_voices_async().get()
        return [
            {
                "name": v.name,
                "locale": v.locale,
                "gender": v.gender,
                "styles": v.style_list,
            }
            for v in voices.voices if v.locale.startswith(locale_prefix)
        ]

    def tts(self, text, voice="fa-IR-DilaraNeural", format="audio-16khz-32kbitrate-mono-mp3", ssml=False):
        """Convert text or SSML to speech and return audio bytes"""
        self.speech_config.speech_synthesis_voice_name = voice

        format_map = {
            "audio-16khz-32kbitrate-mono-mp3": "Audio16Khz32KBitRateMonoMp3",
            "audio-24khz-48kbitrate-mono-mp3": "Audio24Khz48KBitRateMonoMp3",
            "audio-48khz-96kbitrate-mono-mp3": "Audio48Khz96KBitRateMonoMp3",
            "riff-16khz-16bit-mono-pcm": "Riff16Khz16BitMonoPcm",
            "riff-24khz-16bit-mono-pcm": "Riff24Khz16BitMonoPcm",
            "riff-8khz-16bit-mono-pcm": "Riff8Khz16BitMonoPcm",
            "webm-16khz-16bit-mono-opus": "Webm16Khz16BitMonoOpus",
            "ogg-16khz-16bit-mono-opus": "Ogg16Khz16BitMonoOpus",
            "ogg-24khz-16bit-mono-opus": "Ogg24Khz16BitMonoOpus",
        }
        enum_format = format_map.get(format, "Audio16Khz32KBitRateMonoMp3")
        self.speech_config.set_speech_synthesis_output_format(
            getattr(speechsdk.SpeechSynthesisOutputFormat, enum_format)
        )

        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)

        result = synthesizer.speak_ssml_async(text).get() if ssml else synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return result.audio_data
        elif result.reason == speechsdk.ResultReason.Canceled:
            details = result.cancellation_details
            print(f"Azure TTS canceled: {details.reason}, error={details.error_details}")
            raise Exception(f"TTS failed: {details.reason}")
        else:
            raise Exception(f"TTS failed with reason: {result.reason}")
