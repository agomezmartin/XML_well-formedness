import math
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

def calculate_dtp_time(file_type, count, time_per_unit):
    """Calculate the DTP time for different file types and round up to the nearest quarter hour."""
    try:
        time_per_unit = float(time_per_unit)  # Ensure the input is numeric
    except ValueError:
        raise ValueError(self.tr("Time per unit must be a number."))

    # Calculate time in hours
    if file_type == 'word':
        time = (count * time_per_unit) / 60
    elif file_type == 'ppt':
        time = (count * time_per_unit) / 60
    elif file_type == 'pdf':
        time = (count * time_per_unit) / 60
    else:
        raise ValueError(self.tr(f"Unknown file type: {file_type}"))

    # Round up time to the nearest quarter hour (0.25 hours)
    rounded_time = math.ceil(time * 4) / 4

    return rounded_time
