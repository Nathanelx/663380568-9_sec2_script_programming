# agentic-document-automator/src/pdf_tasks.py
import io
import os

from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

from utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)


class PDFTasks:
    """Handles PDF operations (watermark, merge, extract text) for the Document Agent."""

    def __init__(self):
        logger.info("PDFTasks initialized.")

    def _create_text_watermark_page(self, watermark_text, font_size=50, color=(0, 0, 0, 0.2), angle=45):
        """สร้างหน้า PDF ที่มีแค่ข้อความลายน้ำ (หมุนตามมุมที่กำหนด อยู่กลางหน้า) ด้วย reportlab"""
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        r, g, b, a = color
        c.setFillColor(Color(r, g, b, alpha=a))
        c.setFont('Helvetica-Bold', font_size)
        c.translate(width / 2, height / 2)
        c.rotate(angle)
        text_width = c.stringWidth(watermark_text, 'Helvetica-Bold', font_size)
        c.drawString(-text_width / 2, -font_size / 4, watermark_text)
        c.showPage()
        c.save()
        buffer.seek(0)
        logger.info("Generated watermark page.")
        return PdfReader(buffer).pages[0]

    def apply_watermark(self, input_pdf_path, output_pdf_path, watermark_text, font_size=50,
                        color=(0.5, 0.5, 0.5, 0.2), angle=45):
        if not os.path.exists(input_pdf_path):
            logger.error(f"Input PDF for watermarking not found: {input_pdf_path}")
            return False

        ensure_directory_exists(os.path.dirname(output_pdf_path))
        try:
            watermark_page = self._create_text_watermark_page(watermark_text, font_size, color, angle)
            reader = PdfReader(input_pdf_path)
            writer = PdfWriter()
            for page in reader.pages:
                page.merge_page(watermark_page)  # วางลายน้ำทับบนทุกหน้า
                writer.add_page(page)
            with open(output_pdf_path, 'wb') as f:
                writer.write(f)
            logger.info(f"Watermark applied to '{input_pdf_path}'. Output saved to '{output_pdf_path}'.")
            return True
        except Exception as e:
            logger.error(f"Error applying watermark to '{input_pdf_path}': {e}")
            return False

    def merge_pdfs(self, pdf_paths, output_path):
        if not pdf_paths:
            logger.warning("No PDF paths provided for merging.")
            return False
        writer = PdfWriter()
        ensure_directory_exists(os.path.dirname(output_path))
        for pdf_path in pdf_paths:
            if not os.path.exists(pdf_path):
                logger.warning(f"Skipping non-existent PDF for merging: {pdf_path}")
                continue
            try:
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    writer.add_page(page)
                logger.info(f"Added '{pdf_path}' to merge queue.")
            except Exception as e:
                logger.error(f"Error reading PDF '{pdf_path}': {e}")
        if len(writer.pages) == 0:
            logger.warning("No pages were added to the merged PDF.")
            return False
        try:
            with open(output_path, 'wb') as f:
                writer.write(f)
            logger.info(f"PDFs successfully merged to '{output_path}'.")
            return True
        except Exception as e:
            logger.error(f"Error writing merged PDF: {e}")
            return False

    def extract_text_from_pdf(self, pdf_path):
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            return None
        text_content = ""
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                text_content += page.extract_text() + "\n--- Page End ---\n"
            logger.info(f"Text extracted from PDF: {pdf_path}")
            return text_content
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return None
