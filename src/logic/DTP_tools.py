from docx import Document
from pptx import Presentation
import fitz  # PyMuPDF for PDFs

def count_pages_docx(file_path):
    doc = Document(file_path)
    return len(doc.paragraphs)

def count_slides_pptx(file_path):
    ppt = Presentation(file_path)
    return len(ppt.slides)

def count_pages_pdf(file_path):
    pdf = fitz.open(file_path)
    page_count = pdf.page_count
    pdf.close()
    return page_count

def is_editable_pdf(file_path):
    # Placeholder logic for editable PDF detection
    return True
