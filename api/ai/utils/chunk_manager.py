import re
import html
from bs4 import BeautifulSoup

class HTMLChunker:
    def __init__(self):
        """
        Initialize HTMLChunker.
        No arguments required.
        """
        self.TAG_RE = re.compile(r'(<[^>]+>)', re.DOTALL)
        self.ENTITY_RE = re.compile(r'&[A-Za-z0-9#]+;')
        self.BLOCK_BREAK_TAGS = {
            "p", "div", "br", "li", "ul", "ol",
            "h1", "h2", "h3", "h4", "h5", "h6",
            "table", "tr", "th", "td", "thead", "tbody", "tfoot", "pre", "code"
        }
        self._SENT_END_CHARS = ".!?;؟؛…。！？；．।॥։።፧"
        self._CLOSERS = "’”\"'»›）)]】》〗〙〛〉］｝』」"
        self._OPTIONAL_CLOSERS_RE = f"[{re.escape(self._CLOSERS)}]*"
        self._TRAILING_CLOSE_TAGS_RE = r"(?:\s*(?:</[^>]+>))*\s*$"
        self._COMPLETE_SENTENCE_AT_END = re.compile(
            rf"(?:\.{{3}}|[{re.escape(self._SENT_END_CHARS)}]){self._OPTIONAL_CLOSERS_RE}{self._TRAILING_CLOSE_TAGS_RE}"
        )

    def _tag_name(self, tag):
        """
        Extract the tag name from an HTML tag string.
        Args:
            tag (str): HTML tag string (e.g., '<div>', '</p>').
        Returns:
            str: Lowercase tag name (e.g., 'div', 'p').
        """
        m = re.match(r'<\s*/?\s*([a-zA-Z0-9]+)', tag)
        return m.group(1).lower() if m else ""

    def _iter_html_tokens(self, html_src):
        """
        Tokenize HTML into tags and text segments.
        Args:
            html_src (str): HTML source string.
        Yields:
            tuple: ('tag', tag_str) or ('text', text_str)
        """
        pos = 0
        for m in self.TAG_RE.finditer(html_src):
            if m.start() > pos:
                yield ("text", html_src[pos:m.start()])
            yield ("tag", m.group(1))
            pos = m.end()
        if pos < len(html_src):
            yield ("text", html_src[pos:])

    def _iter_text_units(self, raw_text):
        """
        Tokenize raw text into entities and characters.
        Args:
            raw_text (str): Text string.
        Yields:
            tuple: (raw, plain) where raw is the entity/char and plain is the decoded value.
        """
        i = 0
        while i < len(raw_text):
            em = self.ENTITY_RE.match(raw_text, i)
            if em:
                raw = em.group(0)
                try:
                    plain = html.unescape(raw)
                except Exception:
                    plain = raw
                yield raw, plain
                i = em.end()
            else:
                ch = raw_text[i]
                yield ch, ch
                i += 1

    def join_paragraphs(self, text):
        """
        Join all paragraphs into a single line, separating them by a space.
        Args:
            text (str): The input text with paragraphs separated by line breaks.
        Returns:
            str: Text with paragraphs joined by a space.
        """
        # Split into lines, strip each, and filter out empty lines
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        # Join with a space
        return " ".join(lines)
    
    def clean_text(self, text):
        """
        Clean up plain text by stripping leading/trailing spaces and collapsing multiple blank lines.
        Args:
            text (str): The input plain text.
        Returns:
            str: Cleaned text.
        """
        lines = text.splitlines()
        cleaned_lines = []
        last_blank = False
        for line in lines:
            stripped = line.strip()
            if not stripped:
                if not last_blank:
                    cleaned_lines.append("")
                last_blank = True
            else:
                cleaned_lines.append(stripped)
                last_blank = False
        return "\n".join(cleaned_lines)
    
    def get_simple_text_from_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ")
        return text
    
    def chunk_html_streaming(self, html_src, max_text_chars = 1000):
        """
        Chunk HTML into segments of up to max_text_chars, preserving tag structure.
        Args:
            html_src (str): HTML source string.
            max_text_chars (int): Maximum number of text characters per chunk (default: 1000).
        Returns:
            List[Dict[str, str]]: List of chunks, each with 'html' and 'text' keys.
        """
        chunks = []
        html_buf = []
        text_buf = []
        cur_len = 0

        def flush():
            nonlocal html_buf, text_buf, cur_len
            if html_buf or text_buf:
                chunks.append({
                    "html": "".join(html_buf),
                    "text": "".join(text_buf).strip()
                })
            html_buf = []
            text_buf = []
            cur_len = 0

        for kind, token in self._iter_html_tokens(html_src):
            if kind == "tag":
                html_buf.append(token)
                name = self._tag_name(token)
                if name == "br" or token.startswith("</"):
                    if name in self.BLOCK_BREAK_TAGS or name == "br":
                        text_buf.append("\n")
                        cur_len += 1
                continue
            for raw_unit, plain_unit in self._iter_text_units(token):
                if cur_len + len(plain_unit) > max_text_chars and cur_len > 0:
                    flush()
                html_buf.append(raw_unit)
                text_buf.append(plain_unit)
                cur_len += len(plain_unit)
        flush()
        return chunks

    def get_incomplete_end_html_aware(self, chunk_html, backtrack=300, sent_end_chars=None, optional_closers_re=None, complete_sentence_at_end=None):
        """
        Get the complete and incomplete parts at the end of a chunk, ignoring HTML entities as boundaries.
        Args:
            chunk_html (str): HTML chunk string.
            backtrack (int): Number of characters to look back for incomplete segments (default: 300).
            sent_end_chars (str): Sentence-ending characters.
            optional_closers_re (str): Regex for optional closers.
            complete_sentence_at_end (re.Pattern): Compiled regex for complete sentence at end.
        Returns:
            tuple: (head, tail) where head is the complete part and tail is the incomplete part.
        """
        s = chunk_html or ""
        n = len(s)
        if n == 0:
            return "", ""
        # 1. Check for incomplete HTML tag at the end
        last_lt = s.rfind("<")
        last_gt = s.rfind(">")
        if last_lt > last_gt:
            # Incomplete tag at the end
            return s[:last_lt], s[last_lt:]
        # 2. Check for incomplete sentence at the end
        sent_end_chars = sent_end_chars or getattr(self, '_SENT_END_CHARS', ".!?;؟؛…。！？；．।॥։።፧")
        optional_closers_re = optional_closers_re or getattr(self, '_OPTIONAL_CLOSERS_RE', "")
        complete_sentence_at_end = complete_sentence_at_end or getattr(self, '_COMPLETE_SENTENCE_AT_END', None)
        wstart = max(0, n - backtrack)
        if complete_sentence_at_end and complete_sentence_at_end.search(s):
            # Ends with a complete sentence
            return s, ""
        window = s[wstart:n]
        # Only consider true sentence-ending punctuation, not entities or quotes
        true_endings = ".!?؟؛…。！？；．।॥։።፧"  # Remove ; from true_endings
        last_punct = -1
        for idx, char in enumerate(window):
            # Only treat ; as ending if not part of an entity
            if char == ';':
                # Check if part of an entity (e.g., &rsquo;)
                ent_start = window.rfind('&', 0, idx)
                if ent_start != -1 and all(c.isalnum() or c == '#' for c in window[ent_start+1:idx]):
                    continue  # skip ; in entity
                else:
                    last_punct = idx
            elif char in true_endings:
                last_punct = idx
        if last_punct >= 0:
            cut = wstart + last_punct + 1
            # Optionally extend cut to include closers and closing tags
            import re
            m = re.match(optional_closers_re, s[cut:])
            if m and m.end() > 0:
                cut += m.end()
            m2 = re.match(r"(?:\s*(?:</[^>]+>))*\s*", s[cut:])
            if m2 and m2.end() > 0:
                cut += m2.end()
            if cut < n:
                return s[:cut], s[cut:]
        # 3. If no tag or sentence boundary found, treat everything as head
        return s, ""

class ChunkPipeline:
    """
    High-level pipeline for chunking HTML using HTMLChunker.
    """
    def __init__(self, max_text_chars=1000, backtrack=300):
        """
        Initialize ChunkPipeline.
        Args:
            max_text_chars (int): Maximum number of text characters per chunk (default: 1000).
            backtrack (int): Number of characters to look back for incomplete segments (default: 300).
            method (str): Method to use for incomplete sentence detection ('custom' or 'advanced', default: 'advanced').
        """
        self.chunker = HTMLChunker()
        self.max_text_chars = max_text_chars
        self.backtrack = backtrack

    def process(self, html_src, mode="get_chunks", chunk_method="html_aware"):
        """
        Chunk HTML source using HTMLChunker and get complete/incomplete boundaries for each chunk.
        Args:
            html_src (str): HTML source string.
            mode (str): Mode for processing ('get_chunks' or 'get_text', default: 'get_chunks').
                If mode == "get_chunks", chunk HTML.
                If mode == "get_text", return simple text.
            chunk_method (str): Method to use for incomplete sentence detection ('html_aware', default: 'html_aware').
                If chunk_method == "html_aware", use custom logic for incomplete sentence detection.
        Returns:
            List[Dict[str, str]]: List of chunk dicts with 'html', 'text', 'head', and 'tail' keys.
        """
        html_src = self.chunker.clean_text(html_src)
        html_src = self.chunker.join_paragraphs(html_src)
        if mode == "get_text":
            return self.chunker.get_simple_text_from_html(html_src)
        chunks = self.chunker.chunk_html_streaming(html_src, self.max_text_chars)
        results = []
        for chunk in chunks:
            if chunk_method == "html_aware":
                head, tail = self.chunker.get_incomplete_end_html_aware(chunk["html"], self.backtrack)
            results.append({
                "html": chunk["html"],
                "text": chunk["text"],
                "head": head,
                "tail": tail,
            })
        return results