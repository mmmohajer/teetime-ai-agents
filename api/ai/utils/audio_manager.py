from unittest import result
from django.conf import settings
import wave
import io
import subprocess
import tempfile
import uuid

from ai.utils.open_ai_manager import OpenAIManager
class AudioManager:
    def __init__(self):
        """DOC
        Initializes the AudioManager instance.
        No arguments.
        """
        self.open_ai_manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY)

    def preprocess_wav(self, wav_bytes):
        """DOC
        Applies basic preprocessing (noise reduction, bandpass filtering, volume normalization) to WAV audio bytes using ffmpeg.

        Args:
            wav_bytes (bytes): The input audio data in WAV format.

        Returns:
            bytes: The preprocessed audio data in WAV format.
        """
        with tempfile.NamedTemporaryFile(suffix=".wav") as in_file, \
            tempfile.NamedTemporaryFile(suffix=".wav") as out_file:
            in_file.write(wav_bytes)
            in_file.flush()
            # Enhanced filter chain: noise reduction, bandpass, amplitude normalization, volume boost, silence removal
            filter_chain = "afftdn,highpass=f=300,lowpass=f=3400,dynaudnorm,volume=3dB,silenceremove=stop_periods=-1:stop_duration=1:stop_threshold=-50dB"
            cmd = [
                "ffmpeg", "-y", "-i", in_file.name,
                "-af", filter_chain,
                "-ar", "16000", "-ac", "1", "-f", "wav", out_file.name
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                raise RuntimeError(f"ffmpeg preprocessing failed: {result.stderr.decode()}")
            out_file.seek(0)
            return out_file.read()
    
    def convert_webm_to_wav(self, webm_bytes):
        """DOC
        Converts WebM/Opus audio bytes to WAV format using ffmpeg.

        Args:
            webm_bytes (bytes): The input audio data in WebM/Opus format.

        Returns:
            bytes: The converted audio data in WAV format.
        """
        with tempfile.NamedTemporaryFile(suffix=".webm") as webm_file, \
             tempfile.NamedTemporaryFile(suffix=".wav") as wav_file:
            webm_file.write(webm_bytes)
            webm_file.flush()
            cmd = [
                "ffmpeg", "-y", "-i", webm_file.name,
                "-ar", "16000", "-ac", "1", "-f", "wav", wav_file.name
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                raise RuntimeError(f"ffmpeg conversion failed: {result.stderr.decode()}")
            wav_file.seek(0)
            return wav_file.read()

    def create_wav_from_chunk(self, chunk_bytes, sample_width=2, channels=1, framerate=16000):
        """DOC
        Wraps raw PCM audio bytes in a WAV header, or re-creates a WAV file from existing WAV bytes.

        Args:
            chunk_bytes (bytes): The input audio data (raw PCM or WAV).
            sample_width (int): Sample width in bytes (default: 2).
            channels (int): Number of audio channels (default: 1).
            framerate (int): Sample rate in Hz (default: 16000).

        Returns:
            bytes: Audio data in valid WAV format.
        """
        try:
            buffer = io.BytesIO(chunk_bytes)
            with wave.open(buffer, 'rb') as wf:
                params = wf.getparams()
                new_buffer = io.BytesIO()
                with wave.open(new_buffer, 'wb') as new_wf:
                    new_wf.setparams(params)
                    new_wf.writeframes(wf.readframes(params.nframes))
                return new_buffer.getvalue()
        except wave.Error:
            new_buffer = io.BytesIO()
            with wave.open(new_buffer, 'wb') as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(sample_width)
                wf.setframerate(framerate)
                wf.writeframes(chunk_bytes)
            return new_buffer.getvalue()

    def skip_seconds_wav(self, wav_bytes, seconds_to_skip):
        """DOC
        Skips a specified number of seconds from the beginning of a WAV audio byte stream.

        Args:
            wav_bytes (bytes): The input audio data in WAV format.
            seconds_to_skip (float): Number of seconds to skip from the start.

        Returns:
            bytes: WAV audio data with the initial seconds skipped.
        """
        buffer = io.BytesIO(wav_bytes)
        with wave.open(buffer, 'rb') as wf:
            framerate = wf.getframerate()
            sample_width = wf.getsampwidth()
            channels = wf.getnchannels()
            total_frames = wf.getnframes()
            frames_to_skip = int(framerate * seconds_to_skip)
            wf.setpos(frames_to_skip)
            remaining_frames = wf.readframes(total_frames - frames_to_skip)

        out_buffer = io.BytesIO()
        with wave.open(out_buffer, 'wb') as out_wf:
            out_wf.setnchannels(channels)
            out_wf.setsampwidth(sample_width)
            out_wf.setframerate(framerate)
            out_wf.writeframes(remaining_frames)
        return out_buffer.getvalue()
    
    def get_wav_duration(self, wav_bytes):
        """
        Get the duration of a WAV audio byte stream.

        Args:
            wav_bytes (bytes): The input audio data in WAV format.

        Returns:
            float: The duration of the audio in seconds.
        """
        buffer = io.BytesIO(wav_bytes)
        with wave.open(buffer, 'rb') as wf:
            framerate = wf.getframerate()
            total_frames = wf.getnframes()
            duration = total_frames / framerate
        return duration
    
    def limit_wav_duration(self, wav_bytes, max_duration):
        """
        Limits a WAV audio byte stream to max_duration seconds.

        Args:
            wav_bytes (bytes): The input audio data in WAV format.
            max_duration (float): Max duration to keep (in seconds).

        Returns:
            bytes: Truncated WAV audio data.
        """
        buffer = io.BytesIO(wav_bytes)
        with wave.open(buffer, 'rb') as wf:
            framerate = wf.getframerate()
            sample_width = wf.getsampwidth()
            channels = wf.getnchannels()
            max_frames = int(framerate * max_duration)
            wf.setpos(0)
            frames = wf.readframes(max_frames)
        out_buffer = io.BytesIO()
        with wave.open(out_buffer, 'wb') as out_wf:
            out_wf.setnchannels(channels)
            out_wf.setsampwidth(sample_width)
            out_wf.setframerate(framerate)
            out_wf.writeframes(frames)
        return out_buffer.getvalue()
    
    def advanced_stt(self, audio_bytes, duration_in_second_to_skip=0, max_duration=None, progress_callback=None, target_language=None):
        """
        Processes audio input (WebM/Opus bytes), applies preprocessing, runs STT, chunks the text, and improves each chunk using OpenAI. Optionally reports progress via callback.

        Args:
            audio_bytes (bytes): Input audio data in WebM/Opus format.
            duration_in_second_to_skip (float): Number of seconds to skip from the start of the audio.
            progress_callback (callable, optional): Function to call with progress updates. Signature: progress_callback(progress: float, chunk_index: int, total_chunks: int, improved_chunk: str)

        Returns:
            str: The improved speech text reconstructed from all chunks.
        """
        wav_data = self.convert_webm_to_wav(audio_bytes)
        if max_duration:
            wav_data = self.limit_wav_duration(wav_data, max_duration)
        filtered_wav = self.skip_seconds_wav(wav_data, duration_in_second_to_skip)
        open_ai_text = self.open_ai_manager.stt(filtered_wav, input_type='bytes', language=target_language)
        stt_chunks = self.open_ai_manager.build_chunks(text=open_ai_text, max_chunk_size=1000)
        self.open_ai_manager.add_message("system", text=(
            "You are a text fixer for speech-to-text (STT) outputs of the user. "
            "cur_chunk is the USER MESSAGE and may contain transcription errors, misheard words, or awkward phrasing. "
            "TASK: CORRECT ONLY cur_chunk (USER MESSAGE) IF NEEDED TO MAKE IT CLEARER, GRAMMATICALLY FIXED, and NATURAL, "
            "while strictly preserving the original meaning, style, and approximate length of cur_chunk. "
            "Do NOT add new sentences, explanations, or unrelated details to cur_chunk. "
            "If the input of cur_chunk is already correct, return the original text EXACTLY as received, without any change, copy, or reformulation."
        ))
        processed_text = ""
        total_chunks = len(stt_chunks)
        for i, chunk in enumerate(stt_chunks):
            cur_chunk = chunk["text"]
            self.open_ai_manager.add_message("user", text=f"cur_chunk: {cur_chunk}")
            improved_chunk = self.open_ai_manager.generate_response()
            processed_text += improved_chunk + " "
            if progress_callback:
                progress_callback(i, total_chunks, improved_chunk)
        return processed_text.strip()
    
    def convert_audio_bytes_to_wav(self, audio_bytes, input_format=None):
        """
        Converts audio bytes in WebM/Opus, MP3, WAV, or M4A format to WAV bytes using ffmpeg if needed.

        Args:
            audio_bytes (bytes): Input audio data.
            input_format (str, optional): Explicit format ('webm', 'mp3', 'wav', 'm4a'). If None, tries to auto-detect.

        Returns:
            bytes: WAV audio data.
        """
        def detect_format(audio_bytes):
            if audio_bytes[:4] == b'RIFF':
                return 'wav'
            if audio_bytes[:3] == b'ID3' or audio_bytes[0:2] == b'\xff\xfb':
                return 'mp3'
            if audio_bytes[:4] == b'\x1A\x45\xDF\xA3':
                return 'webm'
            if audio_bytes[:4] == b'\x00\x00\x00\x20' or audio_bytes[4:8] == b'ftyp':
                return 'm4a'
            return 'webm'

        fmt = input_format or detect_format(audio_bytes)
        if fmt == 'wav':
            return audio_bytes
        elif fmt == 'mp3':
            with tempfile.NamedTemporaryFile(suffix=".mp3") as mp3_file, \
                tempfile.NamedTemporaryFile(suffix=".wav") as wav_file:
                mp3_file.write(audio_bytes)
                mp3_file.flush()
                cmd = [
                    "ffmpeg", "-y", "-i", mp3_file.name,
                    "-ar", "16000", "-ac", "1", "-f", "wav", wav_file.name
                ]
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode != 0:
                    raise RuntimeError(f"ffmpeg conversion failed: {result.stderr.decode()}")
                wav_file.seek(0)
                return wav_file.read()
        elif fmt == 'm4a':
            with tempfile.NamedTemporaryFile(suffix=".m4a") as m4a_file, \
                tempfile.NamedTemporaryFile(suffix=".wav") as wav_file:
                m4a_file.write(audio_bytes)
                m4a_file.flush()
                cmd = [
                    "ffmpeg", "-y", "-i", m4a_file.name,
                    "-ar", "16000", "-ac", "1", "-f", "wav", wav_file.name
                ]
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode != 0:
                    raise RuntimeError(f"ffmpeg conversion failed: {result.stderr.decode()}")
                wav_file.seek(0)
                return wav_file.read()
        else:
            with tempfile.NamedTemporaryFile(suffix=".webm") as webm_file, \
                tempfile.NamedTemporaryFile(suffix=".wav") as wav_file:
                webm_file.write(audio_bytes)
                webm_file.flush()
                cmd = [
                    "ffmpeg", "-y", "-i", webm_file.name,
                    "-ar", "16000", "-ac", "1", "-f", "wav", wav_file.name
                ]
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode != 0:
                    raise RuntimeError(f"ffmpeg conversion failed: {result.stderr.decode()}")
                wav_file.seek(0)
                return wav_file.read()
    
    def convert_audio_to_text(self, audio_bytes, chunk_duration_sec=60, do_final_edition=False, progress_callback=None, input_format=None, chunk_progress_callback=None, target_language=None):
        """
        Converts audio to text using advanced STT, processing the audio in manageable chunks (default: 1 minute).
        Supports input formats: WebM/Opus, MP3, WAV, M4A. Each chunk is processed sequentially, skipping already processed duration, until the whole audio is transcribed and improved.

        Args:
            audio_bytes (bytes): Input audio data in WebM/Opus, MP3, WAV, or M4A format.
            chunk_duration_sec (int): Duration (in seconds) of each chunk to process (default: 60).
            progress_callback (callable, optional): Function to call with progress updates for each chunk.
            input_format (str, optional): Explicit format ('webm', 'mp3', 'wav', 'm4a'). If None, tries to auto-detect.
            chunk_progress_callback (callable, optional): Function to call with progress updates for each chunk during processing.
            do_final_edition (bool): Whether to perform a final text improvement after all chunks are processed (default: False).

        Returns:
            str: The improved speech text reconstructed from all chunks.
        """
        wav_data = self.convert_audio_bytes_to_wav(audio_bytes, input_format=input_format)
        processed_wav = self.preprocess_wav(wav_data)
        total_duration = self.get_wav_duration(processed_wav)
        processed_text = ""
        num_chunks = int(total_duration // chunk_duration_sec) + (1 if total_duration % chunk_duration_sec > 0 else 0)
        for chunk_idx in range(num_chunks):
            self.open_ai_manager.clear_messages()   
            chunk_text = self.advanced_stt(processed_wav, duration_in_second_to_skip=chunk_idx * chunk_duration_sec, max_duration=chunk_duration_sec * (chunk_idx + 1), progress_callback=chunk_progress_callback, target_language=target_language)
            if progress_callback:
                progress_callback(chunk_idx, num_chunks, chunk_text)
            processed_text += chunk_text + " "
        self.open_ai_manager.clear_messages()
        finalized_text = processed_text.strip()
        if do_final_edition:
            finalized_text = self.open_ai_manager.manipulate_text(text=finalized_text, manipulation_type='improve_awkward_words_or_phrases_for_better_meaning_while_do_your_best_to_preserve_original_text', target_language=target_language)
        return finalized_text