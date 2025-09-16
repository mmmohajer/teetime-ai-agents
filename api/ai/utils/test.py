import base64
from pydoc import text
from django.conf import settings
import json
import os
from google.cloud import texttospeech, speech

from ai.utils.open_ai_manager import OpenAIManager
from ai.utils.google_ai_manager import GoogleAIManager
from ai.utils.ocr_manager import OCRManager
from ai.utils.audio_manager import AudioManager
from ai.utils.aws_manager import AwsManager
from ai.utils.azure_manager import AzureManager

def test_get_response():
    manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY)
    manager.add_message("system", text="You are a helpful assistant, that receives a text and will generate a json including user_message and a random id")
    manager.add_message("system", text="Format of the json is like {'user_message': <user_message>, 'id': <random_id>}")
    manager.add_message("user", text="Hello, world!")
    response = manager.generate_response()
    cost = manager.get_cost()
    json_response = json.loads(response)
    print(json_response['id'])
    print(f"Response: {json.dumps(json_response, indent=2)}")
    print(f"Cost: {cost}")

def test_convert_html_to_text():
    html_file_path = os.path.join(settings.MEDIA_ROOT, 'index.html')
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY)
    simple_text = manager.build_simple_text_from_html(html_content)
    with open(os.path.join(settings.MEDIA_ROOT, 'simple_text.txt'), 'w', encoding='utf-8') as file:
        file.write(simple_text)
    print(f"Successfully Done")

def test_chunking():
    html_file_path = os.path.join(settings.MEDIA_ROOT, 'index.html')
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY)
    chunks = manager.build_chunks(text=html_content, max_chunk_size=1000)
    for i, chunk in enumerate(chunks):
        html_src = chunk["html"]
        simple_text = chunk["text"]
        with open(os.path.join(settings.MEDIA_ROOT, f'chunk_{i}.html'), 'w', encoding='utf-8') as file:
            file.write(html_src)
        with open(os.path.join(settings.MEDIA_ROOT, f'chunk_{i}.txt'), 'w', encoding='utf-8') as file:
            file.write(simple_text)
    print(f"Successfully Done")

def test_ai_tts():
    manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY)
    # Simulate SSML tags for OpenAI TTS
    my_var = "HEY GUYS!!!!!!"
    text = f"""
        "{my_var} ... "
        "I am SO EXCITED to speak with you today. "
        "    This is a demonstration (with a higher pitch) of OpenAI's text-to-speech capabilities. "
        "Can you hear the happiness in my voice? "
        "Let's make this a WONDERFUL EXPERIENCE together!"
    """
    audio_bytes = manager.tts(text=text, voice="nova", audio_format="mp3")
    audio_file_path = os.path.join(settings.MEDIA_ROOT, 'audio.mp3')
    with open(audio_file_path, 'wb') as file:
        file.write(audio_bytes)
    print(manager.get_cost())
    print(f"Successfully Done")

def test_ai_stt():
    manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY)
    audio_file_path = os.path.join(settings.MEDIA_ROOT, 'audio.mp3')
    with open(audio_file_path, 'rb') as file:
        audio_bytes = file.read()
    text = manager.stt(audio_input=audio_bytes, input_type="bytes")
    print(f"Transcribed Text: {text}")

def test_google_add_message():
    manager = GoogleAIManager(api_key=settings.GOOGLE_API_KEY)
    manager.add_message("user", text="Hello, Google!")
    manager.add_message("assistant", text="Hello, How are you?")
    manager.add_message("system", text="You are a helpful assistant.")
    manager.add_message("user", text="Can you tell me a joke?")
    manager.add_message("user", text="This is a joke for you.")
    manager.add_message("system", text="You have to build a joke.")
    print(manager.prompt)

def test_google_generate_response():
    manager = GoogleAIManager(api_key=settings.GOOGLE_API_KEY)
    manager.add_message("user", text="Tell me a joke.")
    response = manager.generate_response()
    print(f"Response: {response}")

def test_google_tts():
    manager = GoogleAIManager(api_key=settings.GOOGLE_API_KEY)
    text = (
        """<speak>\n"
        "Hello, Google!\n"
        "<break time=\"500ms\"/>\n"
        "<emphasis level=\"strong\">This is a demonstration of speech synthesis.</emphasis>\n"
        "<break time=\"300ms\"/>\n"
        "<prosody pitch=\"+2st\" rate=\"slow\">You can control pitch and speaking rate with SSML prosody tags.</prosody>\n"
        "<break time=\"400ms\"/>\n"
        "<prosody pitch=\"-2st\" rate=\"fast\">Now, let's try a lower pitch and faster rate.</prosody>\n"
        "<break time=\"300ms\"/>\n"
        "<emphasis level=\"moderate\">SSML makes your TTS output more expressive!</emphasis>\n"
        "<break time=\"500ms\"/>\n"
        "Thank you for listening.\n"
        "</speak>"""
    )
    audio_bytes = manager.tts(text=text, voice_name="en-US-Wavenet-D", audio_encoding=texttospeech.AudioEncoding.MP3)
    audio_file_path = os.path.join("/websocket_tmp/google_tts", 'tts_audio.mp3')
    with open(audio_file_path, 'wb') as file:
        file.write(audio_bytes)
    print(f"Successfully Done")

def test_google_stt():
    manager = GoogleAIManager(api_key=settings.GOOGLE_API_KEY)
    audio_file_path = os.path.join("/websocket_tmp/google_tts", 'tts_audio.mp3')
    with open(audio_file_path, 'rb') as file:
        audio_bytes = file.read()
        text = manager.stt(
            audio_bytes=audio_bytes,
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            file_path=audio_file_path
        )
    print(manager.get_cost())
    print(f"Transcribed Text: {text}")

def test_document_ai_ocr():
    manager = OCRManager(
        google_cloud_project_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROJECT_ID,
        google_cloud_location=settings.GOOGLE_CLOUD_DOCUMENT_AI_LOCATION,
        google_cloud_processor_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID
    )
    pdf_file_path = os.path.join("/websocket_tmp/texts/", 'The Data Science Handbook.pdf')
    png_bytes = manager.convert_pdf_page_to_png_bytes(pdf_file_path, page_number=21)
    html_output = manager.ocr_using_document_ai(base64.b64encode(png_bytes).decode('utf-8'))
    with open(os.path.join("/websocket_tmp/texts/", 'document_ai_output.html'), 'w', encoding='utf-8') as file:
        file.write(html_output)
    print(f"Successfully Done!")

def test_google_tts_farsi():
    manager = GoogleAIManager(api_key=settings.GOOGLE_API_KEY)
    text = (
        """<speak>\n"
        "سلام، گوگل!\n"
        "<break time=\"500ms\"/>\n"
        "<emphasis level=\"strong\">این یک نمایش از سنتز گفتار است.</emphasis>\n"
        "<break time=\"300ms\"/>\n"
        "<prosody pitch=\"+2st\" rate=\"slow\">شما می‌توانید با برچسب‌های SSML، گام و سرعت گفتار را کنترل کنید.</prosody>\n"
        "<break time=\"400ms\"/>\n"
        "<prosody pitch=\"-2st\" rate=\"fast\">حالا، بیایید یک گام پایین‌تر و سرعت سریع‌تر را امتحان کنیم.</prosody>\n"
        "<break time=\"300ms\"/>\n"
        "<emphasis level=\"moderate\">SSML خروجی TTS شما را بیان‌گرتر می‌کند!</emphasis>\n"
        "<break time=\"500ms\"/>\n"
        "متشکرم که گوش دادید.\n"
        "</speak>"""
    )
    audio_bytes = manager.tts(text=text, voice_name="fa-IR-Standard-A", audio_encoding=texttospeech.AudioEncoding.MP3, language_code="fa-IR")
    audio_file_path = os.path.join("/websocket_tmp/google_tts", 'tts_audio_fa.mp3')
    with open(audio_file_path, 'wb') as file:
        file.write(audio_bytes)
    print(f"Successfully Done")

def list_voices():
     # test_google_tts_farsi()
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices()
    voices_list = []
    for voice in voices.voices:
        voice_info = {
            "name": voice.name,
            "languages": list(voice.language_codes),  # Convert to list for JSON serialization
            "gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        }
        voices_list.append(voice_info)
    with open(os.path.join("/websocket_tmp/google_tts", "voices.json"), "w", encoding="utf-8") as file:
        json.dump(voices_list, file, ensure_ascii=False, indent=2)
    print(f"Wrote {len(voices_list)} voices to voices.json")

def test_summarizer():
    pdf_path = os.path.join("/websocket_tmp/texts/", 'Relativity4.pdf')
    with open(pdf_path, 'rb') as file:
        pdf_bytes = file.read()
    ocr_manager = OCRManager(
        google_cloud_project_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROJECT_ID,
        google_cloud_location=settings.GOOGLE_CLOUD_DOCUMENT_AI_LOCATION,
        google_cloud_processor_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID
    )
    pdf_file_path = os.path.join("/websocket_tmp/texts/", 'Relativity4.pdf')
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()
    number_of_pages = ocr_manager.get_pdf_page_count(pdf_bytes)
    pdf_texts = []
    for page in range(1, number_of_pages + 1):
        print(f"Processing page {page}...")
        png_bytes = ocr_manager.convert_pdf_page_to_png_bytes(pdf_file_path, page_number=page)
        html_output = ocr_manager.ocr_using_document_ai(base64.b64encode(png_bytes).decode('utf-8'))
        open_ai_manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY)
        page_text = open_ai_manager.build_simple_text_from_html(html_output)
        pdf_texts.append(page_text)
    text_to_summarize = "".join(pdf_texts)
    print(f"\n\nLength: {len(text_to_summarize)}\n\n")
    summary = open_ai_manager.summarize(text=text_to_summarize, max_length=1000, max_chunk_size=15000)
    with open(os.path.join("/websocket_tmp/texts/", 'summary.txt'), 'w', encoding='utf-8') as file:
        file.write(summary)

def test_summarizer_for_translation():
    pdf_path = os.path.join("/websocket_tmp/texts/", 'Relativity4.pdf')
    with open(pdf_path, 'rb') as file:
        pdf_bytes = file.read()
    ocr_manager = OCRManager(
        google_cloud_project_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROJECT_ID,
        google_cloud_location=settings.GOOGLE_CLOUD_DOCUMENT_AI_LOCATION,
        google_cloud_processor_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID
    )
    pdf_file_path = os.path.join("/websocket_tmp/texts/", 'Relativity4.pdf')
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()
    number_of_pages = ocr_manager.get_pdf_page_count(pdf_bytes)
    pdf_texts = []
    for page in range(1, number_of_pages + 1):
        print(f"Processing page {page}...")
        png_bytes = ocr_manager.convert_pdf_page_to_png_bytes(pdf_file_path, page_number=page)
        html_output = ocr_manager.ocr_using_document_ai(base64.b64encode(png_bytes).decode('utf-8'))
        open_ai_manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY)
        page_text = open_ai_manager.build_simple_text_from_html(html_output)
        pdf_texts.append(page_text)
    text_to_summarize = "".join(pdf_texts)
    print(f"\n\nLength: {len(text_to_summarize)}\n\n")
    summary = open_ai_manager.summarize_for_translation(text=text_to_summarize, max_length=5000, max_chunk_size=15000)
    with open(os.path.join("/websocket_tmp/texts/", 'summary_translation.txt'), 'w', encoding='utf-8') as file:
        file.write(summary)

def test_translation():
    pdf_path = os.path.join("/websocket_tmp/texts/", 'Relativity4.pdf')
    with open(pdf_path, 'rb') as file:
        pdf_bytes = file.read()
    ocr_manager = OCRManager(
        google_cloud_project_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROJECT_ID,
        google_cloud_location=settings.GOOGLE_CLOUD_DOCUMENT_AI_LOCATION,
        google_cloud_processor_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID
    )
    pdf_file_path = os.path.join("/websocket_tmp/texts/", 'Relativity4.pdf')
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()
    number_of_pages = ocr_manager.get_pdf_page_count(pdf_bytes)
    number_of_pages = 1
    pdf_texts = []
    for page in range(1, number_of_pages + 1):
        print(f"Processing page {page}...")
        png_bytes = ocr_manager.convert_pdf_page_to_png_bytes(pdf_file_path, page_number=page)
        html_output = ocr_manager.ocr_using_document_ai(base64.b64encode(png_bytes).decode('utf-8'))
        open_ai_manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY)
        pdf_texts.append(html_output)
    html_to_translate = "".join(pdf_texts)
    translate = open_ai_manager.translate(html_to_translate, target_language="en")
    with open(os.path.join("/websocket_tmp/texts/", 'translation.html'), 'w', encoding='utf-8') as file:
        file.write(translate)

def test_summarizer_for_manipulation():
    pdf_path = os.path.join("/websocket_tmp/texts/", 'Relativity4.pdf')
    with open(pdf_path, 'rb') as file:
        pdf_bytes = file.read()
    ocr_manager = OCRManager(
        google_cloud_project_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROJECT_ID,
        google_cloud_location=settings.GOOGLE_CLOUD_DOCUMENT_AI_LOCATION,
        google_cloud_processor_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID
    )
    pdf_file_path = os.path.join("/websocket_tmp/texts/", 'Relativity4.pdf')
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()
    number_of_pages = ocr_manager.get_pdf_page_count(pdf_bytes)
    pdf_texts = []
    for page in range(1, number_of_pages + 1):
        print(f"Processing page {page}...")
        png_bytes = ocr_manager.convert_pdf_page_to_png_bytes(pdf_file_path, page_number=page)
        html_output = ocr_manager.ocr_using_document_ai(base64.b64encode(png_bytes).decode('utf-8'))
        open_ai_manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY)
        page_text = open_ai_manager.build_simple_text_from_html(html_output)
        pdf_texts.append(page_text)
    text_to_summarize = "".join(pdf_texts)
    print(f"\n\nLength: {len(text_to_summarize)}\n\n")
    summary = open_ai_manager.summarize_for_manipulation(text=text_to_summarize, manipulation_type="improve_fluency_and_make_it_academic", max_length=5000, max_chunk_size=15000)
    with open(os.path.join("/websocket_tmp/texts/", 'summary_manipulation.txt'), 'w', encoding='utf-8') as file:
        file.write(summary)

def test_manipulation():
    pdf_path = os.path.join("/websocket_tmp/texts/", 'Relativity4.pdf')
    with open(pdf_path, 'rb') as file:
        pdf_bytes = file.read()
    ocr_manager = OCRManager(
        google_cloud_project_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROJECT_ID,
        google_cloud_location=settings.GOOGLE_CLOUD_DOCUMENT_AI_LOCATION,
        google_cloud_processor_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID
    )
    pdf_file_path = os.path.join("/websocket_tmp/texts/", 'Relativity4.pdf')
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()
    number_of_pages = ocr_manager.get_pdf_page_count(pdf_bytes)
    pdf_texts = []
    for page in range(1, number_of_pages + 1):
        print(f"Processing page {page}...")
        png_bytes = ocr_manager.convert_pdf_page_to_png_bytes(pdf_file_path, page_number=page)
        html_output = ocr_manager.ocr_using_document_ai(base64.b64encode(png_bytes).decode('utf-8'))
        open_ai_manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY)
        pdf_texts.append(html_output)
    html_to_translate = "".join(pdf_texts)
    translate = open_ai_manager.manipulate_text(html_to_translate, manipulation_type="improve_fluency_and_make_it_academic", target_language="en")
    with open(os.path.join("/websocket_tmp/texts/", 'manipulation_full.html'), 'w', encoding='utf-8') as file:
        file.write(translate)

def test_html_to_pdf():
    ocr_manager = OCRManager(
        google_cloud_project_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROJECT_ID,
        google_cloud_location=settings.GOOGLE_CLOUD_DOCUMENT_AI_LOCATION,
        google_cloud_processor_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID
    )
    with open(os.path.join("/websocket_tmp/texts/", 'manipulation_full.html'), 'r', encoding='utf-8') as file:
        html_content = file.read()
    pdf_bytes = ocr_manager.convert_html_to_pdf(html_content)
    with open("/websocket_tmp/texts/manipulation_full.pdf", "wb") as f:
        f.write(pdf_bytes)

def test_q_and_a_generation():
    pdf_path = os.path.join("/websocket_tmp/zahra/", 'zahra.pdf')
    with open(pdf_path, 'rb') as file:
        pdf_bytes = file.read()
    ocr_manager = OCRManager(
        google_cloud_project_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROJECT_ID,
        google_cloud_location=settings.GOOGLE_CLOUD_DOCUMENT_AI_LOCATION,
        google_cloud_processor_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID
    )
    pdf_file_path = os.path.join("/websocket_tmp/zahra/", 'zahra.pdf')
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()
    number_of_pages = ocr_manager.get_pdf_page_count(pdf_bytes)
    # number_of_pages = 1
    pdf_texts = []
    for page in range(1, number_of_pages + 1):
        print(f"Processing page {page}...")
        png_bytes = ocr_manager.convert_pdf_page_to_png_bytes(pdf_file_path, page_number=page)
        html_output = ocr_manager.ocr_using_document_ai(base64.b64encode(png_bytes).decode('utf-8'))
        pdf_texts.append(html_output)
    html_to_translate = "".join(pdf_texts)
    open_ai_manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY)
    q_a_list = open_ai_manager.generate_q_and_a_from_text(html_to_translate, target_language="en", max_length_for_general_summary=2000, max_chunk_size_for_general_summary=15000, max_chunk_size=2500, max_q_and_a_tokens=5000)
    with open("/websocket_tmp/texts/q_and_a.json", "w", encoding="utf-8") as f:
        json.dump(q_a_list, f, ensure_ascii=False, indent=2)

def test_multi_choice_q_generation():
    pdf_path = os.path.join("/websocket_tmp/zahra/", 'zahra.pdf')
    with open(pdf_path, 'rb') as file:
        pdf_bytes = file.read()
    ocr_manager = OCRManager(
        google_cloud_project_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROJECT_ID,
        google_cloud_location=settings.GOOGLE_CLOUD_DOCUMENT_AI_LOCATION,
        google_cloud_processor_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID
    )
    pdf_file_path = os.path.join("/websocket_tmp/zahra/", 'zahra.pdf')
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()
    number_of_pages = ocr_manager.get_pdf_page_count(pdf_bytes)
    # number_of_pages = 1
    pdf_texts = []
    for page in range(1, number_of_pages + 1):
        print(f"Processing page {page}...")
        png_bytes = ocr_manager.convert_pdf_page_to_png_bytes(pdf_file_path, page_number=page)
        html_output = ocr_manager.ocr_using_document_ai(base64.b64encode(png_bytes).decode('utf-8'))
        pdf_texts.append(html_output)
    html_to_translate = "".join(pdf_texts)
    open_ai_manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY)
    q_a_list = open_ai_manager.generate_multiple_choice_questions_from_text(html_to_translate, target_language="en", max_length_for_general_summary=2000, max_chunk_size_for_general_summary=15000, max_chunk_size=1000, max_mcq_tokens=5000)
    with open("/websocket_tmp/zahra/multi_choice.json", "w", encoding="utf-8") as f:
        json.dump(q_a_list, f, ensure_ascii=False, indent=2)

def test_teaching_content():
    pdf_path = os.path.join("/websocket_tmp/texts/", 'Relativity4.pdf')
    with open(pdf_path, 'rb') as file:
        pdf_bytes = file.read()
    ocr_manager = OCRManager(
        google_cloud_project_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROJECT_ID,
        google_cloud_location=settings.GOOGLE_CLOUD_DOCUMENT_AI_LOCATION,
        google_cloud_processor_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID
    )
    pdf_file_path = os.path.join("/websocket_tmp/texts/", 'Relativity4.pdf')
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()
    number_of_pages = ocr_manager.get_pdf_page_count(pdf_bytes)
    number_of_pages = 1
    pdf_texts = []
    for page in range(1, number_of_pages + 1):
        print(f"Processing page {page}...")
        png_bytes = ocr_manager.convert_pdf_page_to_png_bytes(pdf_file_path, page_number=page)
        html_output = ocr_manager.ocr_using_document_ai(base64.b64encode(png_bytes).decode('utf-8'))
        pdf_texts.append(html_output)
    html_to_translate = "".join(pdf_texts)
    open_ai_manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY)
    q_a_list = open_ai_manager.build_teaching_content_for_a_text(html_to_translate, target_language="en", max_length_for_general_summary=2000, max_chunk_size_for_general_summary=15000, max_chunk_size=1000, max_teaching_tokens=5000)
    with open("/websocket_tmp/texts/teaching.json", "w", encoding="utf-8") as f:
        json.dump(q_a_list, f, ensure_ascii=False, indent=2)

def test_build_rag_materials_for_text():
    pdf_path = os.path.join("/websocket_tmp/texts/", 'Relativity4.pdf')
    with open(pdf_path, 'rb') as file:
        pdf_bytes = file.read()
    ocr_manager = OCRManager(
        google_cloud_project_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROJECT_ID,
        google_cloud_location=settings.GOOGLE_CLOUD_DOCUMENT_AI_LOCATION,
        google_cloud_processor_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID
    )
    pdf_file_path = os.path.join("/websocket_tmp/texts/", 'Relativity4.pdf')
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()
    number_of_pages = ocr_manager.get_pdf_page_count(pdf_bytes)
    number_of_pages = 1
    pdf_texts = []
    for page in range(1, number_of_pages + 1):
        print(f"Processing page {page}...")
        png_bytes = ocr_manager.convert_pdf_page_to_png_bytes(pdf_file_path, page_number=page)
        html_output = ocr_manager.ocr_using_document_ai(base64.b64encode(png_bytes).decode('utf-8'))
        pdf_texts.append(html_output)
    html_to_translate = "".join(pdf_texts)
    open_ai_manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY)
    rag_materials = open_ai_manager.build_materials_for_rag(text=html_to_translate)
    with open("/websocket_tmp/texts/rag.json", "w", encoding="utf-8") as f:
        json.dump(rag_materials, f, ensure_ascii=False, indent=2)

def test_advanced_stt():
    audio_path = os.path.join("/websocket_tmp/me/", 'chunk_0.wav')
    with open(audio_path, 'rb') as file:
        audio_bytes = file.read()
    audio_manager = AudioManager()
    def progress_callback(chunk_index, total_chunks, improved_chunk):
        print(f"Progress: {chunk_index + 1}/{total_chunks} - {improved_chunk[:30]}...")
    result = audio_manager.advanced_stt(audio_bytes, progress_callback=progress_callback)
    with open("/websocket_tmp/me/advanced_stt_result.txt", "w", encoding="utf-8") as f:
        f.write(result)

def test_convert_audio_to_text():
    audio_path = os.path.join("/websocket_tmp/me/", 'tavalod.m4a')
    with open(audio_path, 'rb') as file:
        audio_bytes = file.read()
    audio_manager = AudioManager()
    def progress_callback(chunk_index, total_chunks, improved_chunk):
        print(f"Progress: {chunk_index + 1}/{total_chunks}")
    def chunk_progress_callback(chunk_index, total_chunks, chunk_text):
        print(f"Chunk Progress: {chunk_index + 1}/{total_chunks}")
    result = audio_manager.convert_audio_to_text(audio_bytes, chunk_duration_sec=30, do_final_edition=True, progress_callback=progress_callback, input_format='m4a', chunk_progress_callback=chunk_progress_callback)
    with open("/websocket_tmp/me/convert_audio_to_text_result_now.html", "w", encoding="utf-8") as f:
        f.write(result)

def test_advanced_teaching_content():
    pdf_path = os.path.join("/websocket_tmp/texts/", 'Relativity4.pdf')
    with open(pdf_path, 'rb') as file:
        pdf_bytes = file.read()
    ocr_manager = OCRManager(
        google_cloud_project_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROJECT_ID,
        google_cloud_location=settings.GOOGLE_CLOUD_DOCUMENT_AI_LOCATION,
        google_cloud_processor_id=settings.GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID
    )
    pdf_file_path = os.path.join("/websocket_tmp/texts/", 'Relativity4.pdf')
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()
    number_of_pages = ocr_manager.get_pdf_page_count(pdf_bytes)
    number_of_pages = 1
    pdf_texts = []
    for page in range(1, number_of_pages + 1):
        print(f"Processing page {page}...")
        png_bytes = ocr_manager.convert_pdf_page_to_png_bytes(pdf_file_path, page_number=page)
        html_output = ocr_manager.ocr_using_document_ai(base64.b64encode(png_bytes).decode('utf-8'))
        pdf_texts.append(html_output)
    html_to_translate = "".join(pdf_texts)
    open_ai_manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY)
    q_a_list = open_ai_manager.build_advanced_teaching_content_for_a_text(html_to_translate, target_language="en", max_length_for_general_summary=2000, max_chunk_size_for_general_summary=15000, max_chunk_size=1000, max_teaching_tokens=5000)
    with open("/websocket_tmp/texts/advanced_teaching.json", "w", encoding="utf-8") as f:
        json.dump(q_a_list, f, ensure_ascii=False, indent=2)

def test_aws_tts():
    aws_manager = AwsManager(
        access_key_id=settings.AWS_ACCESS_KEY_ID,
        secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_DEFAULT_REGION
    )
    text = """
        <speak>
        سلام! به سرویس <emphasis level="strong">پالی</emphasis> خوش آمدید.
        </speak>
    """
    audio_bytes = aws_manager.tts(text=text, voice="Zeina", format="mp3", ssml=True)
    print(f"Available voices: {aws_manager.list_voices(language_code="arb")}")
    audio_file_path = os.path.join("/websocket_tmp/aws_tts", 'aws_tts_audio.mp3')
    with open(audio_file_path, 'wb') as file:
        file.write(audio_bytes)
    print(f"Successfully Done")

def test_azure_tts():
    ssml_text = """
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="fa-IR">
    <voice name="fa-IR-DilaraNeural">
        سلام! امروز می‌خواهیم درباره <emphasis level="strong">ری‌اکت</emphasis> صحبت کنیم.
        <break time="700ms"/>
        ری‌اکت یک کتابخانه جاوااسکریپت است که برای ساخت رابط‌های کاربری پویا استفاده می‌شود.
        <break time="600ms"/>
        یکی از مفاهیم مهم در ری‌اکت، <emphasis level="moderate">کامپوننت</emphasis> است. هر کامپوننت می‌تواند داده‌ها و رفتار مخصوص به خود را داشته باشد.
        <break time="700ms"/>
        حالا بیایید درباره یک هوک معروف در ری‌اکت صحبت کنیم: <emphasis level="strong">useEffect</emphasis>.
        <break time="600ms"/>
        هوک <emphasis level="strong">useEffect</emphasis> به شما اجازه می‌دهد تا کدهایی را اجرا کنید که وابسته به تغییرات داده‌ها یا وضعیت کامپوننت هستند.
        <break time="700ms"/>
        برای مثال، اگر بخواهید بعد از هر بار تغییر یک مقدار، داده‌ای را از سرور دریافت کنید، می‌توانید از <emphasis level="strong">useEffect</emphasis> استفاده کنید.
        <break time="600ms"/>
        این قابلیت باعث می‌شود برنامه‌های ری‌اکت شما پویا و واکنش‌گرا باشند.
        <break time="700ms"/>
        امیدوارم این توضیحات به شما کمک کند تا بهتر با ری‌اکت و هوک <emphasis level="strong">useEffect</emphasis> آشنا شوید.
        <break time="600ms"/>
        از توجه شما سپاسگزارم!
    </voice>
    </speak>
    """
    ssml_text = """
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
        <voice name="en-US-AriaNeural">
            Hello! Today, we are going to talk about <emphasis level="strong">React</emphasis>.
            <break time="700ms"/>
            React is a JavaScript library used for building dynamic user interfaces.
            <break time="600ms"/>
            One of the key concepts in React is the <emphasis level="moderate">component</emphasis>. Each component can have its own data and behavior.
            <break time="700ms"/>
            Now, let's discuss a famous hook in React: <emphasis level="strong">useEffect</emphasis>.
            <break time="600ms"/>
            The <emphasis level="strong">useEffect</emphasis> hook allows you to run code that depends on changes in data or the state of a component.
            <break time="700ms"/>
            For example, if you want to fetch data from a server every time a value changes, you can use <emphasis level="strong">useEffect</emphasis>.
            <break time="600ms"/>
            This feature makes your React applications dynamic and responsive.
            <break time="700ms"/>
            I hope these explanations help you better understand React and the <emphasis level="strong">useEffect</emphasis> hook.
            <break time="600ms"/>
            Thank you for your attention!
        </voice>
        </speak>
    """
    azure_manager = AzureManager(
        key=settings.AZURE_COGNITIVE_SERVICES_KEY_1,
        region=settings.AZURE_COGNITIVE_SERVICES_REGION
    )
    print(azure_manager.list_voices())
    audio_bytes = azure_manager.tts(
        text=ssml_text,
        # voice="fa-IR-FaridNeural",
        voice="en-US-AriaNeural",
        format="audio-16khz-32kbitrate-mono-mp3",
        ssml=True
    )
    audio_file_path = os.path.join("/websocket_tmp/azure_tts", 'azure_tts_audio.mp3')
    with open(audio_file_path, 'wb') as file:
        file.write(audio_bytes)
    print("✅ Saved Persian TTS as azure_fa.mp3")


def test_ai_manager():
   list_voices()