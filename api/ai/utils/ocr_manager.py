import base64
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter
from google.cloud import vision, documentai
from google.api_core.client_options import ClientOptions
from pdf2image import convert_from_bytes
import requests
from PyPDF2 import PdfReader
from weasyprint import HTML

from ai.utils.doc_ai_managr import DocAIManager
from ai.utils.chunk_manager import ChunkPipeline
from ai.tasks import apply_cost_task

class OCRManager:
    def __init__(self, google_cloud_project_id, google_cloud_location, google_cloud_processor_id, cur_users=[]):
        """
        Initializes the OCRManager instance with Google Cloud configuration.

        Args:
            google_cloud_project_id (str): Google Cloud project ID.
            google_cloud_location (str): Google Cloud location (e.g., 'us', 'eu').
            google_cloud_processor_id (str): Document AI processor ID.

        Sets:
            self.cost (float): Stores the cost of the last OCR operation.
        """
        self.GOOGLE_CLOUD_PROJECT_ID = google_cloud_project_id
        self.GOOGLE_CLOUD_LOCATION = google_cloud_location
        self.GOOGLE_CLOUD_PROCESSOR_ID = google_cloud_processor_id
        self.cur_users = cur_users
        self.cost = 0

    def _apply_cost(self, cost, service):
        self.cost += cost
        if self.cur_users:
            user_ids = [user.id for user in self.cur_users]
        apply_cost_task.delay(user_ids, cost, service)

    def _png_bytes_to_pdf_bytes(self, png_bytes):
        """
        Converts PNG image bytes to PDF bytes.

        Args:
            png_bytes (bytes): PNG image data.

        Returns:
            bytes: PDF file data.
        """
        im = Image.open(BytesIO(png_bytes)).convert("RGB")
        out = BytesIO()
        im.save(out, format="PDF", resolution=300.0)
        return out.getvalue()
    
    def _docai_blocks_to_html(self, document):
        """
        Converts Document AI blocks to HTML using DocAIManager.

        Args:
            document: Document AI document object.

        Returns:
            str: HTML representation of the document blocks.
        """
        layout = getattr(document, "document_layout", None)
        if not layout:
            return ""
        blocks = getattr(layout, "blocks", [])
        doc_ai_manager = DocAIManager()
        return doc_ai_manager.render_html_blocks(blocks)

    def convert_html_to_pdf(self, html_content):
        """
        Converts HTML content to PDF bytes.

        Args:
            html_content (str): HTML content to convert.

        Returns:
            bytes: PDF file data.
        """
        pdf_bytes = HTML(string=html_content).write_pdf()
        return pdf_bytes

    def get_cost(self):
        """
        Returns the current cost of OCR processing.

        Returns:
            float: The cost of the last OCR operation.
        """
        return self.cost

    def clear_cost(self):
        """
        Clears the current cost of OCR processing.

        Returns:
            None
        """
        self.cost = 0

    def convert_pdf_page_to_png_bytes(self, source, page_number):
        """
        Converts a single PDF page to PNG image bytes. Accepts a file path, URL, or bytes.

        Args:
            source (str or bytes): PDF file path, URL, or bytes.
            page_number (int): The page number to convert (1-based).

        Returns:
            bytes or None: PNG image data, or None if not found or error.
        """
        pdf_bytes = None
        if isinstance(source, bytes):
            pdf_bytes = source
        elif isinstance(source, str):
            if source.startswith('http://') or source.startswith('https://'):
                try:
                    resp = requests.get(source)
                    resp.raise_for_status()
                    pdf_bytes = resp.content
                except Exception as e:
                    print(f"Error downloading PDF from URL: {e}")
                    return None
            else:
                try:
                    with open(source, 'rb') as file:
                        pdf_bytes = file.read()
                except Exception as e:
                    print(f"Error reading PDF from file: {e}")
                    return None
        else:
            print("Unsupported source type for PDF input.")
            return None
        try:
            pages = convert_from_bytes(pdf_bytes, fmt="png", first_page=page_number, last_page=page_number)
            if pages:
                png_bytes_io = BytesIO()
                pages[0].save(png_bytes_io, format="PNG")
                return png_bytes_io.getvalue()
        except Exception as e:
            print(f"Error converting PDF page to PNG: {e}")
        return None
    
    def get_pdf_page_count(self, pdf_bytes):
        """
        Returns the number of pages in a PDF file.

        Args:
            pdf_bytes (bytes): PDF file data.

        Returns:
            int: Number of pages in the PDF.
        """
        reader = PdfReader(BytesIO(pdf_bytes))
        return len(reader.pages)

    def make_img_more_readable(self, img_bytes):
        """
        Enhances the readability of an image by applying sharpening and contrast enhancement.

        Args:
            img_bytes (bytes): Image data (PNG, JPEG, etc.).

        Returns:
            bytes: Enhanced PNG image data.
        """
        im = Image.open(BytesIO(img_bytes))
        im = im.filter(ImageFilter.SHARPEN)
        enhancer = ImageEnhance.Contrast(im)
        im = enhancer.enhance(1.5)
        out = BytesIO()
        im.save(out, format="PNG")
        return out.getvalue()
    
    def ocr_using_document_ai(self, base64_encoded_file, cost_per_page=0.03):
        """
        Processes an image or PDF file using Google Document AI OCR. If input is image, converts to PDF bytes.
        Supports multi-page PDFs by processing each page individually and concatenating the HTML output.

        Args:
            base64_encoded_file (str): Base64-encoded image or PDF file.
            cost_per_page (float, optional): Cost per page for Document AI OCR (default $0.03).

        Returns:
            str or None: HTML output from Document AI OCR, or None on error.
        Sets:
            self.cost (float): Total cost for the operation.
        """
        try:
            client = documentai.DocumentProcessorServiceClient(
                client_options=ClientOptions(api_endpoint=f"{self.GOOGLE_CLOUD_LOCATION}-documentai.googleapis.com")
            )
            name = client.processor_path(self.GOOGLE_CLOUD_PROJECT_ID, self.GOOGLE_CLOUD_LOCATION, self.GOOGLE_CLOUD_PROCESSOR_ID)
            file_bytes = base64.b64decode(base64_encoded_file)
            html_outputs = []
            num_pages = 1
            mime_type = "application/pdf"
            is_image = False
            try:
                im = Image.open(BytesIO(file_bytes))
                is_image = True
            except Exception:
                is_image = False
            if is_image:
                enhanced_img_bytes = self.make_img_more_readable(file_bytes)
                pdf_bytes = self._png_bytes_to_pdf_bytes(enhanced_img_bytes)
            else:
                try:
                    pages = convert_from_bytes(file_bytes, fmt="png")
                    enhanced_pngs = []
                    for page in pages:
                        png_bytes_io = BytesIO()
                        page.save(png_bytes_io, format="PNG")
                        enhanced_png = self.make_img_more_readable(png_bytes_io.getvalue())
                        enhanced_pngs.append(enhanced_png)
                    # Convert enhanced PNGs back to PDF
                    pdf_images = [Image.open(BytesIO(png)) for png in enhanced_pngs]
                    out_pdf = BytesIO()
                    if pdf_images:
                        pdf_images[0].save(out_pdf, format="PDF", save_all=True, append_images=pdf_images[1:], resolution=300.0)
                        pdf_bytes = out_pdf.getvalue()
                    else:
                        pdf_bytes = file_bytes
                except Exception as e:
                    print(f"Error enhancing PDF pages: {e}")
                    pdf_bytes = file_bytes
            try:
                num_pages = self.get_pdf_page_count(pdf_bytes)
            except Exception:
                num_pages = 1
            try:
                req = documentai.ProcessRequest(
                    name=name,
                    raw_document=documentai.RawDocument(content=pdf_bytes, mime_type=mime_type),
                )
                res = client.process_document(request=req)
                html_output = self._docai_blocks_to_html(res.document)
                html_outputs.append(html_output)
            except Exception as e:
                print(f"Error in Document AI OCR: {e}")
                return None
            self._apply_cost(cost=num_pages * cost_per_page, service="GOOGLE_OCR")
            return "\n".join(html_outputs)
        except Exception as e:
            print(f"Error in Document AI OCR: {e}")
            return None
    
    def read_pdf_bytes(self, pdf_bytes, progress_callback=None, start_page=None, end_page=None):
        """
        Extracts and OCRs pages from a PDF file, returning HTML and plain text.

        Args:
            pdf_bytes (bytes): PDF file data.
            progress_callback (callable, optional): Function called after each page is processed. Signature: (page, total).
            start_page (int, optional): First page to process (1-based). If None, starts from first page.
            end_page (int, optional): Last page to process (1-based, inclusive). If None, ends at last page.

        Behavior:
            - Determines the total number of pages in the PDF.
            - Processes only the pages in the range [start_page, end_page].
            - For each page:
                - Converts the page to PNG bytes.
                - Runs OCR using Document AI and collects HTML output.
                - Calls progress_callback (if provided) after each page.
            - Concatenates all HTML outputs.
            - Extracts plain text from the combined HTML using ChunkPipeline.

        Returns:
            tuple:
                html_src (str): Concatenated HTML output for all processed pages.
                simple_text (str): Extracted plain text from the HTML.
        """
        number_of_pages = self.get_pdf_page_count(pdf_bytes)
        start = start_page if start_page is not None else 1
        end = end_page if end_page is not None else number_of_pages
        if start < 1:
            start = 1
        if end > number_of_pages:
            end = number_of_pages
        pdf_texts = []
        for page in range(start, end + 1):
            msg = f"Processing page {page}/{number_of_pages}..."
            if progress_callback:
                progress_callback(page=page, total=number_of_pages)
            else:
                print(msg)
            png_bytes = self.convert_pdf_page_to_png_bytes(pdf_bytes, page_number=page)
            html_output = self.ocr_using_document_ai(base64.b64encode(png_bytes).decode('utf-8'))
            pdf_texts.append(html_output)
        html_src = "".join(pdf_texts)
        chunk_pipeline = ChunkPipeline()
        simple_text = chunk_pipeline.process(html_src, "get_text")
        return html_src, simple_text