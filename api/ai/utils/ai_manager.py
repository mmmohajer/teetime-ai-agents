import re
import random

from ai.utils.chunk_manager import ChunkPipeline
from ai.tasks import apply_cost_task

class BaseAIManager:
    """
    Base class for AI managers.
    ai_type (str): The type of AI being used (e.g., "open_ai"); options are "open_ai", "google".
    """
    def __init__(self, ai_type="open_ai", cur_users=[]):
        self.messages = []
        self.prompt = ""
        self.cost = 0
        self.ai_type = ai_type
        self.cur_users = cur_users

    def _apply_cost(self, cost, service):
        self.cost += cost
        user_ids = []
        if self.cur_users:
            user_ids = [user.id for user in self.cur_users]
        apply_cost_task.delay(user_ids, cost, service)

    def _clean_code_block(self, response_text):
        pattern = r"^```(?:json|html)?\n?(.*)```$"
        match = re.match(pattern, response_text.strip(), re.DOTALL)
        if match:
            return match.group(1).strip()
        return response_text.strip()
    
    def _random_generator(self, length=16):
        """
        Generate a random string of specified length.
        
        Args:
            length (int): Length of the random string. Default is 16.
        
        Returns:
            str: Randomly generated string.
        
        Example:
            token = self._random_generator(8)
        """
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return "".join(random.choice(characters) for _ in range(length))
    
    def get_cost(self):
        """
        Get the total accumulated cost of API calls.

        Returns:
            float: Total cost in USD.

        Example:
            total = manager.get_cost()
        """
        return self.cost

    def clear_cost(self):
        """
        Reset the accumulated cost to zero.

        Returns:
            None

        Example:
            manager.clear_cost()
        """
        self.cost = 0

    def clear_messages(self):
        """
        Clear the message history.

        Returns:
            None

        Example:
            manager.clear_messages()
        """
        self.messages = []
        self.prompt = ""

    def build_simple_text_from_html(self, html_src):
        """
        Convert HTML content to plain text.
        
        Args:
            html (str): The HTML content to convert.
        
        Returns:
            str: The plain text representation.
        """
        chunk_pipeline = ChunkPipeline()
        text = chunk_pipeline.process(html_src, "get_text")
        return text

    def build_chunks(self, text, max_chunk_size=1000, chunk_mode="html_aware"):
        """
        Chunk text into manageable pieces for processing.
        
        Args:
            text (str): The input text to chunk.
            max_chunk_size (int): Maximum size of each chunk. Default is 1000.
        
        Returns:
            list: List of chunk dicts with 'html' and 'text' keys.
        
        Example:
            chunks = manager.build_chunks(long_text, max_chunk_size=500)
        """
        chunk_pipeline = ChunkPipeline(max_text_chars=max_chunk_size, backtrack=300)
        chunks = chunk_pipeline.process(text, "get_chunks", chunk_mode)
        for i in range(len(chunks) - 1):
            head, tail = chunk_pipeline.chunker.get_incomplete_end_html_aware(chunks[i]["html"])
            if tail:
                chunks[i]["html"] = head
                chunks[i]["text"] = self.build_simple_text_from_html(head)
                chunks[i + 1]["html"] = tail + chunks[i + 1]["html"]
                chunks[i + 1]["text"] = self.build_simple_text_from_html(tail + chunks[i + 1]["text"])
        return chunks
    
    def add_message(self, *args, **kwargs):
        """
        Abstract method for adding a new message to build the prompt.
        Must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement add_message.")

    def generate_response(self, *args, **kwargs):
        """
        Abstract method for generating a response from the AI model.
        Must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement generate_response.")
    
    def summarize(self, text, max_length=1000, max_chunk_size=1000, progress_callback=None):
        """
        Iteratively summarize a long text by processing it chunk by chunk and accumulating the summary.
        For each chunk, the method combines the previous summary (if any) with the current chunk and asks the AI model to summarize them together.
        This process continues for all chunks, so the summary grows and evolves as more of the text is processed.

        Args:
            text (str): The text to summarize.
            max_length (int): Maximum number of tokens for each summary step. Default is 1000.
            max_chunk_size (int): Maximum size of each chunk. Default is 1000.

        Returns:
            str: The final accumulated summary of the entire text.

        Example:
            summary = manager.summarize(long_text)
        """
        if len(text) <= max_length:
            return text
        chunks = self.build_chunks(text, max_chunk_size=max_chunk_size)
        summary = ""
        i = 0
        for chunk in chunks:
            i += 1
            msg = f"Processing chunk {i}/{len(chunks)}"
            if progress_callback:
                progress_callback(chunk=chunk, index=i, total=len(chunks))
            else:
                print(msg)
            input_text = (summary + "\n" + chunk["text"]).strip() if summary else chunk["text"]
            messages = [
                {"role": "system", "content": "You are a summarization expert. Summarize the following text."},
                {"role": "user", "content": input_text}
            ]
            prompt = f"Summarize the following text in at most {max_length} tokens:\n\n{input_text}"
            if self.ai_type == "open_ai":
                response = self.generate_response(max_token=max_length, messages=messages)
            elif self.ai_type == "google":
                response = self.generate_response(max_token=max_length, prompt=prompt)
            summary = response
        return summary
    
    def summarize_for_translation(self, text, max_length=1000, max_chunk_size=1000, progress_callback=None):
        """
        Iteratively summarize and interpret a long text chunk by chunk, accumulating summary and clarifications for translation.
        For each chunk, instruct the AI to:
        - Summarize the chunk and previous summary.
        - Identify any ambiguous phrases or unclear meanings and note them.
        - If context from later chunks clarifies previous ambiguities, update the summary to reflect the improved understanding.
        This helps the translation process by tracking and clarifying phrases as more context is available.

        Args:
            text (str): The text to summarize and interpret for translation.
            max_length (int): Maximum number of tokens for each summary step. Default is 1000.
            max_chunk_size (int): Maximum size of each chunk. Default is 1000.

        Returns:
            str: The final accumulated summary and clarifications for translation.

        Example:
            summary = manager.summarize_for_translation(long_text)
        """
        if len(text) <= max_length:
            return text
        chunks = self.build_chunks(text, max_chunk_size=max_chunk_size)
        summary = ""
        i = 0
        for chunk in chunks:
            i += 1
            msg = f"Processing chunk {i}/{len(chunks)}"
            if progress_callback:
                progress_callback(chunk=chunk, index=i, total=len(chunks))
            else:
                print(msg)
            input_text = (summary + "\n" + chunk["text"]).strip() if summary else chunk["text"]
            system_prompt = (
                "You are a translation assistant. The purpose of this summarization is to provide hints and context needed for better translation of words, phrases, and expressions used in the text, not a general summary. "
                "For the following text, do the following: "
                "1. Summarize only the information relevant for accurate translation. "
                "2. Identify any ambiguous phrases or unclear meanings and note them. "
                "3. If you now understand the meaning of a previously ambiguous phrase, clarify it in this summary. "
                "4. Track and update clarifications as more context is available. "
                "5. Because the text comes from OCR, some words/characters might not be captured properly. If you are suspicious about a word, mention it, suggest what the correct word could be, and write it in a highlighted format (ALL UPPERCASE). In the translation, you can use the suggested correction. "
                "Output only the summary and clarifications that help with translation."
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_text}
            ]
            prompt = (
                "Summarize and interpret the following text in at most {max_length} tokens. "
                "Identify ambiguous phrases and clarify them if possible as context improves. "
                "If you are suspicious about a word due to OCR errors, mention it, suggest the correct word, and write it in ALL UPPERCASE for highlighting.\n\n{input_text}"
            )
            if self.ai_type == "open_ai":
                response = self.generate_response(max_token=max_length, messages=messages)
            elif self.ai_type == "google":
                response = self.generate_response(max_token=max_length, prompt=prompt)
            summary = response
        return summary
    
    def summarize_for_manipulation(self, text, manipulation_type="improve_fluency", max_length=1000, max_chunk_size=1000, progress_callback=None):
        """
        Build a summary and guidance for AI to manipulate documentation, with options for tone, style, and improvement hints.
        For each chunk, instruct the AI to:
        - Summarize the chunk and previous summary.
        - Identify weaknesses, areas for improvement, and provide actionable hints.
        - Suggest how to change tone, style, or structure based on manipulation_type (e.g., academic, formal, informal, conversational, poetic, improve fluency, add citations, etc).
        - Track and update guidance as more context is available.

        Args:
            text (str): The text to summarize and guide for manipulation.
            manipulation_type (str): Desired manipulation style (e.g., 'academic', 'formal', 'informal', 'conversational', 'poetic', 'improve_fluency', 'add_citations').
            max_length (int): Maximum number of tokens for each summary step. Default is 1000.
            max_chunk_size (int): Maximum size of each chunk. Default is 1000.

        Returns:
            str: The final accumulated summary and manipulation guidance.

        Example:
            summary = manager.summarize_for_manipulation(long_text, manipulation_type='academic')
        """
        if len(text) <= max_length:
            return text
        chunks = self.build_chunks(text, max_chunk_size=max_chunk_size)
        summary = ""
        i = 0
        for chunk in chunks:
            i += 1
            msg = f"Processing chunk {i}/{len(chunks)}"
            if progress_callback:
                progress_callback(chunk=chunk, index=i, total=len(chunks))
            else:
                print(msg)
            input_text = (summary + "\n" + chunk["text"]).strip() if summary else chunk["text"]
            system_prompt = (
                f"You are a documentation improvement assistant. The purpose of this summarization is to provide hints and guidance for manipulating the text to better match the desired style: {manipulation_type}. "
                "For the following text, do the following: "
                "1. Summarize only the information relevant for improving or changing the tone, literature, and structure. "
                "2. Identify weaknesses, awkward phrasing, poor punctuation, or lack of fluency, and suggest improvements. "
                "3. If manipulation_type is 'academic', make sure to have clear citations if needed, formal structure, and technical vocabulary. "
                "4. If manipulation_type is 'formal', make the text more professional and polished. "
                "5. If manipulation_type is 'informal' or 'conversational', make the text more relaxed and friendly. "
                "6. If manipulation_type is 'poetic', suggest ways to make the text more lyrical or artistic. "
                "7. For any other manipulation_type, provide specific guidance to achieve the desired style. "
                "8. After each paragraph, add hints about weaknesses and how to improve the text. "
                "9. Because the text comes from OCR, some words/characters might not be captured properly. If you are suspicious about a word, mention it, suggest what the correct word could be, and write it in a highlighted format (ALL UPPERCASE). In the manipulation, you can use the suggested correction. "
                "Output only the summary and actionable guidance for manipulation."
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_text}
            ]
            prompt = (
                f"{system_prompt}\n"
                f"Summarize and provide manipulation guidance for the following text in at most {max_length} tokens. "
                f"Manipulation type: {manipulation_type}. "
                "Identify weaknesses and suggest improvements as context improves.\n\n{input_text}"
            )
            if self.ai_type == "open_ai":
                response = self.generate_response(max_token=max_length, messages=messages)
            elif self.ai_type == "google":
                response = self.generate_response(max_token=max_length, prompt=prompt)
            summary = response
        return summary

    def translate(self, text, target_language, max_length_for_general_summary=2000, max_chunk_size_for_general_summary=15000, max_length_for_translation_summary=5000, max_chunk_size_for_translation_summary=15000, max_chunk_size=1000, max_translation_tokens=5000, progress_callback=None):
        """
        Translate text to the target language using context-aware chunking and translation.

        This method first builds a general summary and a translation-focused summary of the input text. It then splits the text into chunks and translates each chunk individually, providing the previous chunk, current chunk, next chunk, general summary, and translation summary as context for each translation step.

        Special translation rules:
        - If the input is HTML, do not translate or modify any HTML tags; keep them as is, even if incomplete.
        - If a chunk contains suspicious or unrelated words (e.g., OCR errors), skip or replace them with meaningful words/phrases.
        - If a chunk/block is only a page number, page title, or footer, ignore it in the translation.
        - Ensure the translation is fluent and natural for the target language, preserving the original meaning.

        Args:
            text (str): The input text (can be HTML).
            target_language (str): The language code to translate to (e.g., 'en', 'fr', 'fa').
            max_length_for_general_summary (int): Maximum tokens for general summary. Default is 2000.
            max_chunk_size_for_general_summary (int): Maximum chunk size for general summary. Default is 15000.
            max_length_for_translation_summary (int): Maximum tokens for translation summary. Default is 5000.
            max_chunk_size_for_translation_summary (int): Maximum chunk size for translation summary. Default is 15000.
            max_chunk_size (int): Maximum size of each chunk for translation. Default is 1000.
            max_translation_tokens (int): Maximum tokens for each translation step. Default is 5000.

        Returns:
            str: The translated text.

        Example:
            translated = manager.translate(text, target_language='en')
        """
        general_summary = self.summarize(text, max_length=max_length_for_general_summary, max_chunk_size=max_chunk_size_for_general_summary)
        translation_summary = self.summarize_for_translation(text, max_length=max_length_for_translation_summary, max_chunk_size=max_chunk_size_for_translation_summary)
        chunks = self.build_chunks(text, max_chunk_size=max_chunk_size)
        translated_chunks = []
        for i, chunk in enumerate(chunks):
            msg = f"Translating chunk {i}/{len(chunks)}"
            if progress_callback:
                progress_callback(chunk=chunk, index=i, total=len(chunks))
            else:
                print(msg)
            previous_chunk = chunks[i-1]["html"] if i > 0 else ""
            cur_chunk = chunk["html"]
            next_chunk = chunks[i+1]["html"] if i < len(chunks)-1 else ""
            system_prompt = (
                f"You are a professional translator. Your task is to translate only the current chunk to {target_language}.\n"
                "You are given the general summary, translation summary, previous chunk, current chunk, and next chunk for context.\n"
                "Do NOT translate or modify any HTML tags; keep them as is, even if incomplete.\n"
                "If you see suspicious/unrelated words (e.g., OCR errors), skip or replace them with meaningful words/phrases.\n"
                "If a chunk/block is only a page number, page title, or footer, ignore it in the translation.\n"
                "Make sure the translation is fluent and natural for the target language, preserving the original meaning."
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": (
                    f"General summary: {general_summary}\n"
                    f"Translation summary: {translation_summary}\n"
                    f"Previous chunk: {previous_chunk}\n"
                    f"Current chunk: {cur_chunk}\n"
                    f"Next chunk: {next_chunk}\n"
                )}
            ]
            if self.ai_type == "open_ai":
                translated = self.generate_response(max_token=max_translation_tokens, messages=messages)
            elif self.ai_type == "google":
                prompt = (
                    f"{system_prompt}\n"
                    f"General summary: {general_summary}\n"
                    f"Translation summary: {translation_summary}\n"
                    f"Previous chunk: {previous_chunk}\n"
                    f"Current chunk: {cur_chunk}\n"
                    f"Next chunk: {next_chunk}\n"
                )
                translated = self.generate_response(max_token=max_translation_tokens, prompt=prompt)
            translated_chunks.append(translated)
        return "".join(translated_chunks)

    def manipulate_text(self, text, manipulation_type="improve_fluency", target_language=None, max_length_for_general_summary=2000, max_chunk_size_for_general_summary=15000, max_length_for_manipulation_summary=5000, max_chunk_size_for_manipulation_summary=15000, max_chunk_size=1000, max_manipulation_tokens=5000, progress_callback=None):
        """
        Manipulate the input text using context-aware chunking, summaries, and generate HTML output with allowed tags and placeholders.

        This method first builds a general summary and a manipulation-focused summary of the input text. It then splits the text into chunks and manipulates each chunk individually, providing the previous chunk, current chunk, next chunk, general summary, manipulation summary, previous manipulated chunk, and a summary of all previous manipulated chunks as context for each manipulation step.

        The output is in HTML format, using only allowed tags: h1-h6, p, div, a, ul, li, img, video. Images and videos use placeholders with captions.

        Args:
            text (str): The input text to manipulate.
            manipulation_type (str): Desired manipulation style (e.g., 'academic', 'formal', 'informal', 'conversational', 'poetic', 'improve_fluency', 'add_citations').
            target_language (str or None): If set, rewrite the improved version in this language (e.g., 'en', 'fr', 'fa'). If None, keep the original language.
            max_length_for_general_summary (int): Maximum tokens for general summary. Default is 2000.
            max_chunk_size_for_general_summary (int): Maximum chunk size for general summary. Default is 15000.
            max_length_for_manipulation_summary (int): Maximum tokens for manipulation summary. Default is 5000.
            max_chunk_size_for_manipulation_summary (int): Maximum chunk size for manipulation summary. Default is 15000.
            max_chunk_size (int): Maximum size of each chunk for manipulation. Default is 1000.
            max_manipulation_tokens (int): Maximum tokens for each manipulation step. Default is 5000.

        Returns:
            str: The manipulated text in HTML format.

        Example:
            manipulated = manager.manipulate_text(text, manipulation_type='academic', target_language='fr')
        """
        general_summary = self.summarize(text, max_length=max_length_for_general_summary, max_chunk_size=max_chunk_size_for_general_summary)
        manipulation_summary = self.summarize_for_manipulation(text, manipulation_type=manipulation_type, max_length=max_length_for_manipulation_summary, max_chunk_size=max_chunk_size_for_manipulation_summary)
        chunks = self.build_chunks(text, max_chunk_size=max_chunk_size)
        manipulated_chunks = []
        joint_manipulated_summary = ""
        for i, chunk in enumerate(chunks):
            msg = f"Manipulating chunk {i}/{len(chunks)}"
            if progress_callback:
                progress_callback(chunk=chunk, index=i, total=len(chunks))
            else:
                print(msg)
            previous_chunk = chunks[i-1]["html"] if i > 0 else ""
            cur_chunk = chunk["html"]
            next_chunk = chunks[i+1]["html"] if i < len(chunks)-1 else ""
            previous_manipulated_chunk = manipulated_chunks[i-1] if i > 0 else ""
            system_prompt = (
                f"You are a professional documentation editor. Your task is to manipulate only the current chunk according to the style: {manipulation_type}.\n"
                + (f"Rewrite the improved version in {target_language}.\n" if target_language else "")
                + "You are given the general summary, manipulation summary, previous chunk, current chunk, next chunk, previous manipulated chunk, and a summary of all previous manipulated chunks for context.\n"
                + "Include only standard HTML tags.\n"
                + "For images or videos, use a placeholder with a caption.\n"
                + "When reviewing each chunk, use the context to improve writing, consistency, and interpretation.\n"
                + "If you see a header, anchor, paragraph, list, or table, use the correct HTML tag.\n"
                + "IMPORTANT: Keep the structure of sentences as is. If the original chunk contains questions, lists, or other formats, preserve those formats in the manipulated output. Do not change questions to statements, or lists to paragraphs, etc.\n"
                + "Output onlsy the manipulated chunk in HTML format."
            )
            user_content = (
                f"General summary: {general_summary}\n"
                f"Manipulation summary: {manipulation_summary}\n"
                f"Previous chunk: {previous_chunk}\n"
                f"Current chunk: {cur_chunk}\n"
                f"Next chunk: {next_chunk}\n"
                f"Previous manipulated chunk: {previous_manipulated_chunk}\n"
                f"Summary of all previous manipulated chunks: {joint_manipulated_summary}\n"
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
            prompt = (
                f"{system_prompt}\n"
                f"General summary: {general_summary}\n"
                f"Manipulation summary: {manipulation_summary}\n"
                f"Previous chunk: {previous_chunk}\n"
                f"Current chunk: {cur_chunk}\n"
                f"Next chunk: {next_chunk}\n"
                f"Previous manipulated chunk: {previous_manipulated_chunk}\n"
                f"Summary of all previous manipulated chunks: {joint_manipulated_summary}\n"
            )
            if self.ai_type == "open_ai":
                manipulated = self.generate_response(max_token=max_manipulation_tokens, messages=messages)
            elif self.ai_type == "google":
                manipulated = self.generate_response(max_token=max_manipulation_tokens, prompt=prompt)
            manipulated_chunks.append(manipulated)
            joint_manipulated_summary = self.summarize(joint_manipulated_summary)
        return "".join(manipulated_chunks)

    def generate_q_and_a_from_text(self, text, target_language=None, max_length_for_general_summary=2000, max_chunk_size_for_general_summary=15000, max_chunk_size=2500, max_q_and_a_tokens=5000, progress_callback=None):
        """
        Generate Q&A pairs from the text to help people understand the context, prepare for exams/interviews, and cover important concepts.

        The method first creates a general summary, then splits the text into chunks. For each chunk, it asks the AI to generate a list of Q&A JSONs:
        [{"question": "STH", "answer": "STH"}, ...]
        Only meaningful, teaching, or explanatory parts should generate Q&A; unimportant sections (e.g., table of contents) should return an empty list.
        For each chunk, the AI receives the last chunk, current chunk, next chunk, general summary, and the summary of previous Q&As for context.

        All questions and answers must be written in the target language if specified.

        Args:
            text (str): The input text (book, article, etc.)
            target_language (str or None): If set, write all questions and answers in this language (e.g., 'en', 'fr', 'fa'). If None, keep the original language.
            max_length_for_general_summary (int): Max tokens for general summary. Default 2000.
            max_chunk_size_for_general_summary (int): Max chunk size for general summary. Default 15000.
            max_chunk_size (int): Max size of each chunk for Q&A. Default 1000.
            max_q_and_a_tokens (int): Max tokens for each Q&A step. Default 2000.

        Returns:
            list: List of Q&A dicts for all chunks.

        Example:
            q_and_a_list = manager.generate_q_and_a_from_text(text, target_language='fr')
        """
        general_summary = self.summarize(text, max_length=max_length_for_general_summary, max_chunk_size=max_chunk_size_for_general_summary)
        chunks = self.build_chunks(text, max_chunk_size=max_chunk_size)
        all_q_and_a = []
        for i, chunk in enumerate(chunks):
            msg = f"Generating Q&A for chunk {i}/{len(chunks)}"
            if progress_callback:
                progress_callback(chunk=chunk, index=i, total=len(chunks))
            else:
                print(msg)
            previous_chunk = chunks[i-1]["html"] if i > 0 else ""
            cur_chunk = chunk["html"]
            next_chunk = chunks[i+1]["html"] if i < len(chunks)-1 else ""
            system_prompt = (
                "You are an expert educator and exam/interview designer. Your task is to generate a list of Q&A pairs in JSON format for the current chunk, to help people understand the context, prepare for exams/interviews, and cover important concepts.\n"
                "Only generate Q&A for meaningful, teaching, or explanatory parts. If the chunk is not important (e.g., table of contents, filler, or lacks concepts), return an empty list.\n"
                "For each Q&A, use the format: {\"question\": \"...\", \"answer\": \"...\"}.\n"
                + (f"All questions and answers must be written in {target_language}.\n" if target_language else "")
                + "You are given the general summary, previous chunk, current chunk, next chunk, for context. These inputs are only helpers to give you better insight and help you analyze the current chunk more effectively.\n"
                + "Output is ONLY for the current chunk. Output only the list of Q&A JSONs."
            )
            user_content = (
                f"General summary: {general_summary}\n"
                f"Previous chunk: {previous_chunk}\n"
                f"Current chunk: {cur_chunk}\n"
                f"Next chunk: {next_chunk}\n"
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
            prompt = (
                f"{system_prompt}\n"
                f"General summary: {general_summary}\n"
                f"Previous chunk: {previous_chunk}\n"
                f"Current chunk: {cur_chunk}\n"
                f"Next chunk: {next_chunk}\n"
            )
            if self.ai_type == "open_ai":
                response = self.generate_response(max_token=max_q_and_a_tokens, messages=messages)
            elif self.ai_type == "google":
                response = self.generate_response(max_token=max_q_and_a_tokens, prompt=prompt)
            try:
                q_and_a_list = eval(response) if isinstance(response, str) else response
                if not isinstance(q_and_a_list, list):
                    q_and_a_list = []
            except Exception:
                q_and_a_list = []
            all_q_and_a.extend(q_and_a_list)
        return all_q_and_a
    
    def generate_multiple_choice_questions_from_text(self, text, target_language=None, max_length_for_general_summary=2000, max_chunk_size_for_general_summary=15000, max_chunk_size=2500, max_mcq_tokens=5000, progress_callback=None):
        """
        Generate multiple-choice questions (MCQs) from the text. Each question has 4 options, only one valid answer.

        The output format for each MCQ:
        {
            "question": "Q",
            "options": [
                {"option": "OPTION1", "is_correct": 1},
                {"option": "OPTION2", "is_correct": 0},
                {"option": "OPTION3", "is_correct": 0},
                {"option": "OPTION4", "is_correct": 0}
            ]
        }
        If the correct answer is "all of the above", only that option is marked as correct and the rest as incorrect.
        All questions and options must be written in the target language if specified.

        Args:
            text (str): The input text (book, article, etc.)
            target_language (str or None): If set, write all questions and options in this language (e.g., 'en', 'fr', 'fa'). If None, keep the original language.
            max_length_for_general_summary (int): Max tokens for general summary. Default 2000.
            max_chunk_size_for_general_summary (int): Max chunk size for general summary. Default 15000.
            max_chunk_size (int): Max size of each chunk for MCQ. Default 2500.
            max_mcq_tokens (int): Max tokens for each MCQ step. Default 5000.

        Returns:
            list: List of MCQ dicts for all chunks.

        Example:
            mcq_list = manager.generate_multiple_choice_questions_from_text(text, target_language='en')
        """
        general_summary = self.summarize(text, max_length=max_length_for_general_summary, max_chunk_size=max_chunk_size_for_general_summary)
        chunks = self.build_chunks(text, max_chunk_size=max_chunk_size)
        all_mcq = []
        for i, chunk in enumerate(chunks):
            msg = f"Generating MCQ for chunk {i}/{len(chunks)}"
            if progress_callback:
                progress_callback(chunk=chunk, index=i, total=len(chunks))
            else:
                print(msg)
            previous_chunk = chunks[i-1]["html"] if i > 0 else ""
            cur_chunk = chunk["html"]
            next_chunk = chunks[i+1]["html"] if i < len(chunks)-1 else ""
            system_prompt = (
                "You are an expert educator and exam/interview designer. Your task is to generate a list of multiple-choice questions (MCQs) in JSON format for the current chunk, to help people understand the context, prepare for exams/interviews, and cover important concepts.\n"
                "Each question must have exactly 4 options, and only one option must be marked as correct (is_correct: 1), the rest as incorrect (is_correct: 0).\n"
                "If the correct answer is 'all of the above', only that option is marked as correct and the rest as incorrect.\n"
                "For each MCQ, use the format: {\"question\": \"...\", \"options\": [{\"option\": \"...\", \"is_correct\": 1/0}, ...]}\n"
                + (f"All questions and options must be written in {target_language}.\n" if target_language else "")
                + "Only generate MCQs for meaningful, teaching, or explanatory parts. If the chunk is not important (e.g., table of contents, filler, or lacks concepts), return an empty list.\n"
                + "You are given the general summary, previous chunk, current chunk, next chunk, for context. These inputs are only helpers to give you better insight and help you analyze the current chunk more effectively.\n"
                + "Output is ONLY for the current chunk. Output only the list of MCQ JSONs."
            )
            user_content = (
                f"General summary: {general_summary}\n"
                f"Previous chunk: {previous_chunk}\n"
                f"Current chunk: {cur_chunk}\n"
                f"Next chunk: {next_chunk}\n"
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
            prompt = (
                f"{system_prompt}\n"
                f"General summary: {general_summary}\n"
                f"Previous chunk: {previous_chunk}\n"
                f"Current chunk: {cur_chunk}\n"
                f"Next chunk: {next_chunk}\n"
            )
            if self.ai_type == "open_ai":
                response = self.generate_response(max_token=max_mcq_tokens, messages=messages)
            elif self.ai_type == "google":
                response = self.generate_response(max_token=max_mcq_tokens, prompt=prompt)
            try:
                mcq_list = eval(response) if isinstance(response, str) else response
                if not isinstance(mcq_list, list):
                    mcq_list = []
            except Exception:
                mcq_list = []
            all_mcq.extend(mcq_list)
        return all_mcq
    
    def build_teaching_content_for_a_text(self, text, target_language=None, max_length_for_general_summary=2000, max_chunk_size_for_general_summary=15000, max_chunk_size=2500, max_teaching_tokens=5000, progress_callback=None):
        """
        Build teaching content for a text. For each chunk, generate:
        {
            "clarifying_concept_to_teach": "HTML output clarifying the concept",
            "q_and_a_list": [{"question": "...", "answer": "..."}, ...]
        }
        The AI must deeply understand each chunk, clarify the concept in HTML, and provide Q&A pairs that ensure mastery of the concept.
        All outputs must be in the target language if specified.

        Args:
            text (str): The input text (book, article, etc.)
            target_language (str or None): If set, write all outputs in this language (e.g., 'en', 'fr', 'fa'). If None, keep the original language.
            max_length_for_general_summary (int): Max tokens for general summary. Default 2000.
            max_chunk_size_for_general_summary (int): Max chunk size for general summary. Default 15000.
            max_chunk_size (int): Max size of each chunk for teaching. Default 2500.
            max_teaching_tokens (int): Max tokens for each teaching step. Default 5000.

        Returns:
            list: List of teaching content dicts for all chunks.

        Example:
            teaching_content = manager.build_teaching_content_for_a_text(text, target_language='en')
        """
        general_summary = self.summarize(text, max_length=max_length_for_general_summary, max_chunk_size=max_chunk_size_for_general_summary)
        chunks = self.build_chunks(text, max_chunk_size=max_chunk_size)
        all_teaching_content = []
        for i, chunk in enumerate(chunks):
            msg = f"Generating teaching content for chunk {i}/{len(chunks)}"
            if progress_callback:
                progress_callback(chunk=chunk, index=i, total=len(chunks))
            else:
                print(msg)
            previous_chunk = chunks[i-1]["html"] if i > 0 else ""
            cur_chunk = chunk["html"]
            next_chunk = chunks[i+1]["html"] if i < len(chunks)-1 else ""
            system_prompt = (
                "You are an expert teacher and educator. For the current chunk, deeply understand the content and generate teaching material as follows:\n"
                "1. clarifying_concept_to_teach: Write a clear, detailed HTML output that explains the concept, using headings, lists, examples, and formatting to help the user learn.\n"
                "2. q_and_a_list: Generate a list of Q&A pairs (question and answer) that, if answered correctly, prove the user has mastered the concept.\n"
                + (f"All outputs must be written in {target_language}.\n" if target_language else "")
                + "Only generate teaching content for meaningful, teaching, or explanatory parts. If the chunk is not important (e.g., table of contents, filler, or lacks concepts), return an empty list.\n"
                + "You are given the general summary, previous chunk, current chunk, next chunk, for context. These inputs are only helpers to give you better insight and help you analyze the current chunk more effectively.\n"
                + "Output is ONLY for the current chunk. Output only the teaching content JSON."
            )
            user_content = (
                f"General summary: {general_summary}\n"
                f"Previous chunk: {previous_chunk}\n"
                f"Current chunk: {cur_chunk}\n"
                f"Next chunk: {next_chunk}\n"
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
            prompt = (
                f"{system_prompt}\n"
                f"General summary: {general_summary}\n"
                f"Previous chunk: {previous_chunk}\n"
                f"Current chunk: {cur_chunk}\n"
                f"Next chunk: {next_chunk}\n"
            )
            if self.ai_type == "open_ai":
                response = self.generate_response(max_token=max_teaching_tokens, messages=messages)
            elif self.ai_type == "google":
                response = self.generate_response(max_token=max_teaching_tokens, prompt=prompt)
            try:
                teaching_content = eval(response) if isinstance(response, str) else response
                if not isinstance(teaching_content, dict):
                    teaching_content = {}
            except Exception:
                teaching_content = {}
            all_teaching_content.append(teaching_content)
        return all_teaching_content
    
    def build_advanced_teaching_content_for_a_text(self, text, target_language=None, max_length_for_general_summary=2000, max_chunk_size_for_general_summary=15000, max_chunk_size=2500, max_teaching_tokens=5000, progress_callback=None):
        """
        Build advanced teaching content for a text. For each chunk, generate:
        {
            "text_for_speech": "Speech the AI teacher will make to explain concepts",
            "text_to_write": "HTML output (like slides) to help user grasp the speech, with highlights, lists, headings, tables, etc.",
            "questions_and_answers": [{"question": "...", "answer": "..."}, ...]
        }
        IMPORTANT: ALL OUTPUTS (text_to_speech, text_to_write, questions_and_answers) MUST BE IN THE TARGET LANGUAGE, EVEN IF THE ORIGINAL LANGUAGE OF THE INPUT IS DIFFERENT. THIS REQUIREMENT IS MANDATORY. IF target_language IS SET, OUTPUTS MUST BE IN THAT LANGUAGE. (REQUIREMENT: ALL OUTPUTS IN TARGET LANGUAGE)

        Args:
            text (str): The input text (book, article, etc.)
            target_language (str or None): If set, write all outputs in this language (e.g., 'en', 'fr', 'fa'). If None, keep the original language.
            max_length_for_general_summary (int): Max tokens for general summary. Default 2000.
            max_chunk_size_for_general_summary (int): Max chunk size for general summary. Default 15000.
            max_chunk_size (int): Max size of each chunk for teaching. Default 2500.
            max_teaching_tokens (int): Max tokens for each teaching step. Default 5000.

        Returns:
            list: List of advanced teaching content dicts for all chunks.
        """
        general_summary = self.summarize(text, max_length=max_length_for_general_summary, max_chunk_size=max_chunk_size_for_general_summary)
        chunks = self.build_chunks(text, max_chunk_size=max_chunk_size)
        all_advanced_content = []
        for i, chunk in enumerate(chunks):
            msg = f"Generating advanced teaching content for chunk {i}/{len(chunks)}"
            if progress_callback:
                progress_callback(chunk=chunk, index=i, total=len(chunks))
            else:
                print(msg)
            previous_chunk = chunks[i-1]["html"] if i > 0 else ""
            cur_chunk = chunk["html"]
            next_chunk = chunks[i+1]["html"] if i < len(chunks)-1 else ""
            system_prompt = (
                "You are an expert AI teacher. For the current chunk, deeply understand the content and generate advanced teaching material as follows:\n"
                "1. text_to_speech: Write a strong, clear explanation for the AI teacher to speak, using SSML markup tags (such as <speak>, <break>, <emphasis>, etc.) to enhance text-to-speech output (e.g., pauses, emphasis, pitch, rate, etc.).\n"
                "2. text_to_write: Write a concise HTML output (like PowerPoint slides) that highlights and organizes the most important points from the speech. Use headings, lists, tables, and formatting to help the user grasp the speech. Do not make it lengthy; focus on clarity and highlights.\n"
                "3. questions_and_answers: Generate a list of Q&A pairs (question and answer) that, if answered correctly, prove the user has mastered the concept.\n"
                + (f"ALL OUTPUTS (text_to_speech, text_to_write, questions_and_answers) MUST BE IN THE {target_language}, EVEN IF THE ORIGINAL LANGUAGE OF THE INPUT IS DIFFERENT. THIS REQUIREMENT IS MANDATORY.\n" if target_language else "")
                + "Only generate teaching content for meaningful, teaching, or explanatory parts. If the chunk is not important (e.g., table of contents, filler, or lacks concepts), return an empty list.\n"
                + "You are given the general summary, previous chunk, current chunk, next chunk, for context. These inputs are only helpers to give you better insight and help you analyze the current chunk more effectively.\n"
                + "Output is ONLY for the current chunk. Output only the advanced teaching content JSON in the following format:\n"
                + '{"text_to_speech": "...", "text_to_write": "...", "questions_and_answers": [{"question": "...", "answer": "..."}, ...]}'
            )
            user_content = (
                f"General summary: {general_summary}\n"
                f"Previous chunk: {previous_chunk}\n"
                f"Current chunk: {cur_chunk}\n"
                f"Next chunk: {next_chunk}\n"
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
            prompt = (
                f"{system_prompt}\n"
                f"General summary: {general_summary}\n"
                f"Previous chunk: {previous_chunk}\n"
                f"Current chunk: {cur_chunk}\n"
                f"Next chunk: {next_chunk}\n"
            )
            if self.ai_type == "open_ai":
                response = self.generate_response(max_token=max_teaching_tokens, messages=messages)
            elif self.ai_type == "google":
                response = self.generate_response(max_token=max_teaching_tokens, prompt=prompt)
            try:
                advanced_content = eval(response) if isinstance(response, str) else response
                if not isinstance(advanced_content, dict):
                    advanced_content = {}
            except Exception:
                advanced_content = {}
            all_advanced_content.append(advanced_content)
        return all_advanced_content
        