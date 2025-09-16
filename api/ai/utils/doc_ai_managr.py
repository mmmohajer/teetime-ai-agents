import html
import re

class DocAIManager:
    """
    DocAIManager provides utilities for processing and rendering structured document blocks (from Google Document AI or similar sources) into HTML.
    It includes noise filtering, heading mapping, text extraction, and table/image rendering.
    """
    def __init__(self):
        """
        Initializes DocAIManager with compiled regex patterns for noise filtering.
        """
        self._FOOTER_RE = re.compile(r"^\s*\d+\s*/\s*\d+\s*$")
        self._DOTS_RE = re.compile(r"^[.\u2026]+$")

    def _is_noise_line(self, t):
        """
        Determines if a line of text is considered noise (empty, footer, dots, bullets).

        Args:
            t (str): The text line to check.

        Returns:
            bool: True if the line is noise, False otherwise.
        """
        t = (t or "").strip()
        if not t:
            return True
        if self._FOOTER_RE.match(t):
            return True
        if self._DOTS_RE.match(t):
            return True
        if t in ("•", "-"):
            return True
        return False
    
    def _map_heading_tag(self, type_text):
        """
        Maps a block type string to an HTML heading tag (h1-h6), or returns None if not a heading.

        Args:
            type_text (str): The type string (e.g., 'heading-1', 'header', 'title').

        Returns:
            str or None: The HTML tag name (e.g., 'h2'), or None if not a heading.
        """
        t = (type_text or "").lower()
        if t.startswith("heading-"):
            try:
                n = int(t.split("-")[1])
                n = min(max(n, 1), 6)
                return f"h{n}"
            except Exception:
                return "h2"
        if t in ("header", "title"):
            return "h2"
        return None
    
    def _text_from_blocks(self, blocks):
        """
        Recursively extracts and concatenates text from a list of blocks.

        Args:
            blocks (list): List of block objects (may have 'text_block' or nested 'blocks').

        Returns:
            str: Concatenated text from all blocks.
        """
        parts = []
        for b in blocks or []:
            tb = getattr(b, "text_block", None)
            if tb and getattr(tb, "text", None):
                parts.append(tb.text)
            child_b = getattr(b, "blocks", None)
            if child_b:
                parts.append(self._text_from_blocks(child_b))
            if tb:
                child_tb = getattr(tb, "blocks", None)
                if child_tb:
                    parts.append(self._text_from_blocks(child_tb))
        return " ".join(p.strip() for p in parts if p and p.strip())
    
    def _render_table(self, table_block):
        """
        Renders a table block into HTML table markup.

        Args:
            table_block: An object representing a table (with header_rows, body_rows, and cell spans).

        Returns:
            str: HTML string for the table.
        """
        def row_html(row, cell_tag="td"):
            cells_html = []
            for cell in getattr(row, "cells", []) or []:
                txt = self._text_from_blocks(getattr(cell, "blocks", None))
                attrs = []
                if getattr(cell, "row_span", 1) > 1:
                    attrs.append(f'rowspan="{cell.row_span}"')
                if getattr(cell, "col_span", 1) > 1:
                    attrs.append(f'colspan="{cell.col_span}"')
                attr_str = (" " + " ".join(attrs)) if attrs else ""
                cells_html.append(f"<{cell_tag}{attr_str}>{html.escape((txt or '').strip())}</{cell_tag}>")
            return "<tr>" + "".join(cells_html) + "</tr>"
        out = ["<table>"]
        hdrs = getattr(table_block, "header_rows", None)
        if hdrs:
            out.append("<thead>")
            for hr in hdrs:
                out.append(row_html(hr, "th"))
            out.append("</thead>")
        out.append("<tbody>")
        for br in getattr(table_block, "body_rows", []) or []:
            out.append(row_html(br, "td"))
        out.append("</tbody></table>")
        return "".join(out)
    
    def render_html_blocks(self, blocks):
        """
        Renders a list of document blocks into HTML, handling tables, images, headings, lists, and paragraphs.

        Args:
            blocks (list): List of block objects from Document AI or similar sources.

        Returns:
            str: HTML string representing the rendered document.
        """
        out = []
        i = 0
        n = len(blocks or [])
        while i < n:
            b = blocks[i]
            tb = getattr(b, "table_block", None)
            if tb:
                out.append(self._render_table(tb))
                i += 1
                continue
            ib = getattr(b, "image_block", None)
            if ib:
                uri = getattr(ib, "image_uri", None)
                if uri:
                    out.append(f"<img src='{html.escape(uri)}' alt='Document image'/>")
                i += 1
                continue
            x = getattr(b, "text_block", None)
            if x:
                raw = (getattr(x, "text", "") or "").strip()
                ttype = (getattr(x, "type_", "") or "").lower()
                if ttype in ("footer", "page-number"):
                    i += 1
                    continue
                if self._is_noise_line(raw):
                    i += 1
                    continue
                if raw.startswith(("•", "-")):
                    items = []
                    while i < n:
                        b2 = blocks[i]
                        x2 = getattr(b2, "text_block", None)
                        if not x2:
                            break
                        t2 = (getattr(x2, "text", "") or "").strip()
                        if not t2.startswith(("•", "-")):
                            break
                        items.append(f"<li>{html.escape(t2.lstrip('•-').strip())}</li>")
                        i += 1
                    out.append("<ul>" + "".join(items) + "</ul>")
                    continue

                tag = self._map_heading_tag(ttype)
                esc = html.escape(raw)
                if tag:
                    out.append(f"<{tag}>{esc}</{tag}>")
                elif ttype in ("caption", "figcaption"):
                    out.append(f"<figcaption>{esc}</figcaption>")
                else:
                    out.append(f"<p>{esc}</p>")
                child_blocks = getattr(b, "blocks", None)
                if child_blocks:
                    out.append(self.render_html_blocks(child_blocks))
                tb_child = getattr(x, "blocks", None)
                if tb_child:
                    out.append(self.render_html_blocks(tb_child))
                i += 1
                continue
            child_blocks = getattr(b, "blocks", None)
            if child_blocks:
                out.append(self.render_html_blocks(child_blocks))
            i += 1
        return "".join(out)
